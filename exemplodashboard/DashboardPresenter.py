"""
Dashboard Presenter - Handles dashboard business logic
"""
from datetime import datetime, timedelta
import threading
from typing import Dict, List, Any
from src.presenters.base.BasePresenter import BasePresenter
from src.services.VendasService import VendasService
from src.services.EstoqueService import EstoqueService
from src.models.Usuario import Usuario
from src.utils.logger import get_logger

logger = get_logger()


class DashboardPresenter(BasePresenter):
    """
    Presenter for Dashboard - coordinates data fetching and calculations
    """
    
    def __init__(self, view, usuario: Usuario):
        """
        Initialize dashboard presenter
        
        Args:
            view: DashboardView instance
            usuario: Current logged in user
        """
        super().__init__(view)
        self.usuario = usuario
        self.vendas_service = VendasService()
        self.estoque_service = EstoqueService()
    
    def on_view_ready(self):
        """Load dashboard data when view is ready"""
        # Load data asynchronously to avoid blocking UI during initialization
        # Dashboard UI appears immediately, data loads 100ms after
        if hasattr(self.view, 'winfo_toplevel'):
            self.view.winfo_toplevel().after(100, self.load_dashboard_data)
        else:
            self.load_dashboard_data()
    
    def load_dashboard_data(self):
        """
        Fetch all dashboard data and update view asynchronously
        """
        # Show loading state
        if hasattr(self.view, 'show_loading'):
            self.view.show_loading()
            
        # Start background thread
        threading.Thread(target=self._fetch_data_thread, daemon=True).start()

    def _fetch_data_thread(self):
        """Background thread to fetch data"""
        try:
            logger.info("[DashboardPresenter] Iniciando carregamento de dados (Background)...")
            
            # Get date range
            hoje = datetime.now().date()
            ontem = hoje - timedelta(days=1)
            
            # Fetch sales data
            vendas_hoje = self.vendas_service.obter_vendas_periodo(hoje, hoje)
            vendas_ontem = self.vendas_service.obter_vendas_periodo(ontem, ontem)
            
            # Calculate metrics
            metrics = self._calculate_metrics(vendas_hoje, vendas_ontem)
            
            # Fetch low stock products
            baixo_estoque = self.estoque_service.listar_produtos_estoque_baixo()
            metrics['qtd_baixo_estoque'] = len(baixo_estoque)
            
            # Fetch expired/expiring products
            vencidos = self.estoque_service.listar_produtos_vencidos()
            vencendo = self.estoque_service.listar_produtos_vencendo()
            metrics['qtd_vencidos'] = len(vencidos)
            metrics['qtd_vencendo'] = len(vencendo)
            metrics['lista_vencidos'] = vencidos  # Passar lista para detalhes se necessário
            
            # Get recent sales for list
            recent_sales = sorted(vendas_hoje, key=lambda x: x.data_hora, reverse=True)[:10]
            
            # Schedule UI update on main thread
            self.view.after(0, lambda: self._on_data_loaded(metrics, recent_sales))
            
        except Exception as e:
            logger.error(f"Erro ao carregar dados dashboard: {e}", exc_info=True)
            self.view.after(0, lambda: self._on_load_error(str(e)))

    def _on_data_loaded(self, metrics, recent_sales):
        """Update UI with loaded data (Main Thread)"""
        try:
            logger.debug("[DashboardPresenter] Atualizando view com dados...")
            self.view.update_metrics(metrics)
            self.view.update_recent_sales(recent_sales)
            
            # Hide loading state
            if hasattr(self.view, 'hide_loading'):
                self.view.hide_loading()
            
            # Show alert if low stock
            if metrics['qtd_baixo_estoque'] > 0:
                self.view.show_low_stock_alert(metrics['qtd_baixo_estoque'])
            
            # Show alert if expired products
            if metrics.get('qtd_vencidos', 0) > 0 or metrics.get('qtd_vencendo', 0) > 0:
                if hasattr(self.view, 'show_expired_alert'):
                    self.view.show_expired_alert(metrics.get('qtd_vencidos', 0), metrics.get('qtd_vencendo', 0))
            
            logger.info("[DashboardPresenter] Dados carregados com sucesso!")
            
        except Exception as e:
            self._on_load_error(str(e))

    def _on_load_error(self, error_msg):
        """Handle load error on main thread"""
        if hasattr(self.view, 'hide_loading'):
            self.view.hide_loading()
        self.view.show_error("Erro", f"Erro ao carregar dashboard: {error_msg}")
    
    
    def _calculate_metrics(self, vendas_hoje: List, vendas_ontem: List) -> Dict[str, Any]:
        """
        Calculate dashboard metrics
        
        Args:
            vendas_hoje: Today's sales list
            vendas_ontem: Yesterday's sales list
            
        Returns:
            Dictionary with calculated metrics
        """
        # Filter completed sales
        vendas_hoje_concluidas = [v for v in vendas_hoje if v.status == 'concluida']
        vendas_ontem_concluidas = [v for v in vendas_ontem if v.status == 'concluida']
        
        # Calculate totals
        total_vendas = sum(v.total for v in vendas_hoje_concluidas)
        total_vendas_ontem = sum(v.total for v in vendas_ontem_concluidas)
        
        qtd_pedidos = len(vendas_hoje_concluidas)
        qtd_pedidos_ontem = len(vendas_ontem_concluidas)
        
        # Calculate variations
        if total_vendas_ontem > 0:
            variacao_vendas = ((total_vendas - total_vendas_ontem) / total_vendas_ontem) * 100
        else:
            variacao_vendas = 100 if total_vendas > 0 else 0
        
        if qtd_pedidos_ontem > 0:
            variacao_pedidos = ((qtd_pedidos - qtd_pedidos_ontem) / qtd_pedidos_ontem) * 100
        else:
            variacao_pedidos = 100 if qtd_pedidos > 0 else 0
        
        return {
            'total_vendas': total_vendas,
            'variacao_vendas': variacao_vendas,
            'qtd_pedidos': qtd_pedidos,
            'variacao_pedidos': variacao_pedidos,
        }
    
    def get_greeting(self) -> tuple[str, str]:
        """
        Get greeting based on current time
        
        Returns:
            Tuple of (greeting_text, emoji)
        """
        hora_atual = datetime.now().hour
        if hora_atual < 12:
            return ("Bom dia", "☀️")
        elif hora_atual < 18:
            return ("Boa tarde", "🌤️")
        else:
            return ("Boa noite", "🌙")
    
    def get_user_display_name(self) -> str:
        """
        Get user's display name
        
        Returns:
            User's full name or username
        """
        if hasattr(self.usuario, 'nome_completo') and self.usuario.nome_completo:
            return self.usuario.nome_completo
        return self.usuario.username

    def get_calendar_events(self, date_obj) -> List[Dict[str, Any]]:
        """
        Get events for calendar (sales on that day)
        
        Args:
            date_obj: Date object to fetch events for
            
        Returns:
            List of event dictionaries
        """
        try:
            # Define start and end of the day
            start = datetime.combine(date_obj, datetime.min.time())
            end = datetime.combine(date_obj, datetime.max.time())
            
            vendas = self.vendas_service.obter_vendas_periodo(start, end)
            
            events = []
            for venda in vendas:
                if venda.status == 'concluida':
                    events.append({
                        'time': venda.data_hora.strftime("%H:%M"),
                        'title': f"Venda #{venda.id} - R$ {venda.total:.2f} ({venda.forma_pagamento})",
                        'type': 'sale'
                    })
            
            return events
        except Exception as e:
            logger.error(f"Erro ao buscar eventos do calendário: {e}")
            return []
