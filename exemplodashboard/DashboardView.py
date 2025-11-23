"""
Dashboard View - Pure UI for dashboard screen
"""
import customtkinter as ctk
from datetime import datetime
from typing import List, Dict, Any, Callable
from src.views.base.BaseView import BaseView
from src.ui import Theme, QuickAccessCard


class DashboardView(BaseView):
    """
    Dashboard View - Renders dashboard UI with no business logic
    """
    
    def __init__(self, parent, on_pdv_click: Callable, on_produtos_click: Callable, 
                 on_estoque_click: Callable, get_calendar_events: Callable = None, **kwargs):
        """
        Initialize dashboard view
        
        Args:
            parent: Parent widget
            on_pdv_click: Callback for PDV button
            on_produtos_click: Callback for products button
            on_estoque_click: Callback for stock button
            get_calendar_events: Callback to fetch events for a date
        """
        super().__init__(parent, fg_color="transparent", **kwargs)
        self.on_pdv_click = on_pdv_click
        self.on_produtos_click = on_produtos_click
        self.on_estoque_click = on_estoque_click
        self.get_calendar_events = get_calendar_events
        
        # UI Components (created in _build_ui)
        self.greeting_label = None
        self.datetime_label = None
        self.alert_frame = None
        self.vendas_value_label = None
        self.vendas_trend_label = None
        self.pedidos_value_label = None
        self.pedidos_trend_label = None
        self.estoque_value_label = None
        self.estoque_status_label = None
        self.recent_sales_container = None
    
    def _build_ui(self):
        """Build the dashboard UI"""
        self._build_header()
        self._build_cards_section()
        self._build_main_grid()
    
    def _build_header(self):
        """Build header with greeting and datetime"""
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill='x', pady=(0, 15))
        
        # Greeting (will be set by presenter)
        self.greeting_label = ctk.CTkLabel(
            header,
            text="",
            font=ctk.CTkFont(size=Theme.FONTS["size_3xl"], weight="bold"),
            text_color=Theme.COLORS["text_primary"]
        )
        self.greeting_label.pack(side='left')
        
        # Date and time
        data_hora = datetime.now().strftime("%d de %B de %Y • %H:%M")
        # Date and time
        data_hora = datetime.now().strftime("%d de %B de %Y • %H:%M")
        self.datetime_label = ctk.CTkLabel(
            header,
            text=data_hora,
            font=ctk.CTkFont(size=Theme.FONTS["size_md"]),
            text_color=Theme.COLORS["text_secondary"],
            cursor="hand2"
        )
        self.datetime_label.pack(side='right', anchor="s")
        
        # Make it clickable
        self.datetime_label.bind("<Button-1>", self._open_calendar)
        
    def _open_calendar(self, event=None):
        """Open calendar dialog"""
        from src.views.dialogs.CalendarDialog import CalendarDialog
        CalendarDialog(self.winfo_toplevel(), self.get_calendar_events)
    
    def _build_cards_section(self):
        """Build metrics cards section"""
        # Container for cards
        cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        cards_frame.pack(fill='x', pady=(0, 30))
        cards_frame.grid_columnconfigure(0, weight=1)
        cards_frame.grid_columnconfigure(1, weight=1)
        cards_frame.grid_columnconfigure(2, weight=1)
        
        # Card 1: Sales
        card1 = ctk.CTkFrame(cards_frame, fg_color=Theme.COLORS["bg_secondary"], corner_radius=15)
        card1.grid(row=0, column=0, padx=10, sticky="ew")
        
        ctk.CTkLabel(
            card1,
            text="💰  Vendas Hoje",
            font=ctk.CTkFont(size=Theme.FONTS["size_md"]),
            text_color=Theme.COLORS["text_secondary"]
        ).pack(padx=20, pady=(15, 5), anchor="w")
        
        self.vendas_value_label = ctk.CTkLabel(
            card1,
            text="R$ 0,00",
            font=ctk.CTkFont(size=Theme.FONTS["size_2xl"], weight="bold"),
            text_color=Theme.COLORS["success"]
        )
        self.vendas_value_label.pack(padx=20, pady=(0, 5), anchor="w")
        
        self.vendas_trend_label = ctk.CTkLabel(
            card1,
            text="",
            font=ctk.CTkFont(size=Theme.FONTS["size_sm"]),
            text_color=Theme.COLORS["text_secondary"]
        )
        self.vendas_trend_label.pack(padx=20, pady=(0, 15), anchor="w")
        
        # Card 2: Orders
        card2 = ctk.CTkFrame(cards_frame, fg_color=Theme.COLORS["bg_secondary"], corner_radius=15)
        card2.grid(row=0, column=1, padx=10, sticky="ew")
        
        ctk.CTkLabel(
            card2,
            text="🛍️  Pedidos",
            font=ctk.CTkFont(size=Theme.FONTS["size_md"]),
            text_color=Theme.COLORS["text_secondary"]
        ).pack(padx=20, pady=(15, 5), anchor="w")
        
        self.pedidos_value_label = ctk.CTkLabel(
            card2,
            text="0",
            font=ctk.CTkFont(size=Theme.FONTS["size_2xl"], weight="bold"),
            text_color=Theme.COLORS["primary"]
        )
        self.pedidos_value_label.pack(padx=20, pady=(0, 5), anchor="w")
        
        self.pedidos_trend_label = ctk.CTkLabel(
            card2,
            text="",
            font=ctk.CTkFont(size=Theme.FONTS["size_sm"]),
            text_color=Theme.COLORS["text_secondary"]
        )
        self.pedidos_trend_label.pack(padx=20, pady=(0, 15), anchor="w")
        
        # Card 3: Low Stock
        card3 = ctk.CTkFrame(cards_frame, fg_color=Theme.COLORS["bg_secondary"], corner_radius=15)
        card3.grid(row=0, column=2, padx=10, sticky="ew")
        
        ctk.CTkLabel(
            card3,
            text="⚠️  Baixo Estoque",
            font=ctk.CTkFont(size=Theme.FONTS["size_md"]),
            text_color=Theme.COLORS["text_secondary"]
        ).pack(padx=20, pady=(15, 5), anchor="w")
        
        self.estoque_value_label = ctk.CTkLabel(
            card3,
            text="0",
            font=ctk.CTkFont(size=Theme.FONTS["size_2xl"], weight="bold"),
            text_color=Theme.COLORS["success"]
        )
        self.estoque_value_label.pack(padx=20, pady=(0, 5), anchor="w")
        
        self.estoque_status_label = ctk.CTkLabel(
            card3,
            text="Normal",
            font=ctk.CTkFont(size=Theme.FONTS["size_sm"]),
            text_color=Theme.COLORS["success"]
        )
        self.estoque_status_label.pack(padx=20, pady=(0, 15), anchor="w")
    
    def _build_main_grid(self):
        """Build main grid with quick actions and recent activity"""
        main_grid = ctk.CTkFrame(self, fg_color="transparent")
        main_grid.pack(fill='both', expand=True)
        main_grid.grid_columnconfigure(0, weight=1)
        main_grid.grid_columnconfigure(1, weight=2)
        
        # Left column: Quick Actions
        left_col = ctk.CTkFrame(main_grid, fg_color="transparent")
        left_col.grid(row=0, column=0, sticky="nsew", padx=(0, 20))
        
        ctk.CTkLabel(
            left_col,
            text="Acesso Rápido",
            font=ctk.CTkFont(size=Theme.FONTS["size_xl"], weight="bold")
        ).pack(anchor="w", pady=(0, 15))
        
        QuickAccessCard(left_col, "🛒", "Nova Venda (PDV)", self.on_pdv_click, Theme.COLORS["success"]).pack(fill="x", pady=8)
        QuickAccessCard(left_col, "📦", "Cadastrar Produto", self.on_produtos_click, Theme.COLORS["primary"]).pack(fill="x", pady=8)
        QuickAccessCard(left_col, "➕", "Entrada Estoque", self.on_estoque_click, Theme.COLORS["warning"]).pack(fill="x", pady=8)
        
        # Right column: Recent Activity
        right_col = ctk.CTkFrame(main_grid, fg_color=Theme.COLORS["bg_secondary"], corner_radius=15)
        right_col.grid(row=0, column=1, sticky="nsew")
        
        header_recent = ctk.CTkFrame(right_col, fg_color="transparent")
        header_recent.pack(fill='x', padx=20, pady=15)
        
        ctk.CTkLabel(
            header_recent,
            text="Últimas Vendas",
            font=ctk.CTkFont(size=Theme.FONTS["size_xl"], weight="bold")
        ).pack(side="left")
        
        # Scrollable container for sales
        self.recent_sales_container = ctk.CTkScrollableFrame(right_col, fg_color="transparent")
        self.recent_sales_container.pack(fill='both', expand=True, padx=10, pady=10)
    
    def set_greeting(self, greeting: str, emoji: str, user_name: str):
        """
        Set greeting text
        
        Args:
            greeting: Greeting text (e.g., "Bom dia")
            emoji: Emoji for the greeting
            user_name: User's display name
        """
        self.greeting_label.configure(text=f"{emoji} {greeting}, {user_name}!")
    
    def update_metrics(self, metrics: Dict[str, Any]):
        """
        Update dashboard metrics cards
        
        Args:
            metrics: Dictionary with metrics data
        """
        # Sales
        total_vendas = metrics.get('total_vendas', 0.0)
        variacao_vendas = metrics.get('variacao_vendas', 0.0)
        self.vendas_value_label.configure(text=f"R$ {total_vendas:.2f}")
        
        seta = "↑" if variacao_vendas >= 0 else "↓"
        cor_variacao = Theme.COLORS["success"] if variacao_vendas >= 0 else Theme.COLORS["danger"]
        self.vendas_trend_label.configure(
            text=f"{seta} {abs(variacao_vendas):.1f}% vs ontem",
            text_color=cor_variacao
        )
        
        # Orders
        qtd_pedidos = metrics.get('qtd_pedidos', 0)
        variacao_pedidos = metrics.get('variacao_pedidos', 0.0)
        self.pedidos_value_label.configure(text=str(qtd_pedidos))
        
        seta = "↑" if variacao_pedidos >= 0 else "↓"
        cor_variacao = Theme.COLORS["success"] if variacao_pedidos >= 0 else Theme.COLORS["danger"]
        self.pedidos_trend_label.configure(
            text=f"{seta} {abs(variacao_pedidos):.1f}% vs ontem",
            text_color=cor_variacao
        )
        
        # Low Stock
        qtd_baixo_estoque = metrics.get('qtd_baixo_estoque', 0)
        cor_estoque = Theme.COLORS["warning"] if qtd_baixo_estoque > 0 else Theme.COLORS["success"]
        status_text = "Crítico" if qtd_baixo_estoque > 10 else "Normal" if qtd_baixo_estoque == 0 else "Atenção"
        
        self.estoque_value_label.configure(text=str(qtd_baixo_estoque), text_color=cor_estoque)
        self.estoque_status_label.configure(text=status_text, text_color=cor_estoque)
    
    def show_low_stock_alert(self, qtd_baixo_estoque: int):
        """
        Show low stock alert banner
        
        Args:
            qtd_baixo_estoque: Number of products with low stock
        """
        if self.alert_frame:
            self.alert_frame.destroy()
        
        self.alert_frame = ctk.CTkFrame(self, fg_color=Theme.COLORS["warning"], corner_radius=10)
        self.alert_frame.pack(fill='x', pady=(0, 20), padx=2, before=self.winfo_children()[1])
        
        alert_content = ctk.CTkFrame(self.alert_frame, fg_color="transparent")
        alert_content.pack(fill='x', padx=15, pady=12)
        
        ctk.CTkLabel(
            alert_content,
            text=f"⚠️  ATENÇÃO: {qtd_baixo_estoque} produto{'s' if qtd_baixo_estoque > 1 else ''} com estoque baixo!",
            font=ctk.CTkFont(size=Theme.FONTS["size_lg"], weight="bold"),
            text_color="#000000"
        ).pack(side='left')
        
        ctk.CTkButton(
            alert_content,
            text="Ver Detalhes",
            command=self.on_estoque_click,
            fg_color="#000000",
            hover_color="#333333",
            width=120,
            height=32
        ).pack(side='right')
    
    def show_expired_alert(self, qtd_vencidos: int, qtd_vencendo: int):
        """
        Show expired products alert banner
        
        Args:
            qtd_vencidos: Number of expired products
            qtd_vencendo: Number of products expiring soon
        """
        # Create a new frame for this alert if it doesn't exist, or reuse/stack
        # For simplicity, let's add another frame below the low stock one if it exists,
        # or just create a new one.
        
        # We'll use a specific attribute for this alert to manage it
        if hasattr(self, 'expired_alert_frame') and self.expired_alert_frame:
            self.expired_alert_frame.destroy()
            
        cor_fundo = Theme.COLORS["danger"] if qtd_vencidos > 0 else Theme.COLORS["warning"]
        texto = ""
        if qtd_vencidos > 0:
            texto = f"⛔ {qtd_vencidos} produto{'s' if qtd_vencidos > 1 else ''} VENCIDO{'S' if qtd_vencidos > 1 else ''}!"
            if qtd_vencendo > 0:
                texto += f" (+{qtd_vencendo} vencendo)"
        else:
            texto = f"⚠️ {qtd_vencendo} produto{'s' if qtd_vencendo > 1 else ''} vencendo em breve!"
            
        self.expired_alert_frame = ctk.CTkFrame(self, fg_color=cor_fundo, corner_radius=10)
        # Pack it before the cards section (which is usually index 1 or 2 depending on header)
        # We want it at the top. Let's pack it after header.
        self.expired_alert_frame.pack(fill='x', pady=(0, 10), padx=2, before=self.winfo_children()[1])
        
        alert_content = ctk.CTkFrame(self.expired_alert_frame, fg_color="transparent")
        alert_content.pack(fill='x', padx=15, pady=12)
        
        ctk.CTkLabel(
            alert_content,
            text=texto,
            font=ctk.CTkFont(size=Theme.FONTS["size_lg"], weight="bold"),
            text_color="#FFFFFF"
        ).pack(side='left')
        
        ctk.CTkButton(
            alert_content,
            text="Ver Produtos",
            command=self.on_produtos_click, # Redirect to products view
            fg_color="#FFFFFF",
            text_color=cor_fundo,
            hover_color="#EEEEEE",
            width=120,
            height=32
        ).pack(side='right')
    
    def update_recent_sales(self, sales: List):
        """
        Update recent sales list
        
        Args:
            sales: List of sale objects
        """
        # Clear existing items
        for widget in self.recent_sales_container.winfo_children():
            widget.destroy()
        
        if not sales:
            # Show empty placeholder
            self._show_empty_sales_placeholder()
        else:
            # Show sales items
            for venda in sales:
                self._create_sale_item(venda)
    
    def _show_empty_sales_placeholder(self):
        """Show placeholder when no sales exist"""
        empty_frame = ctk.CTkFrame(self.recent_sales_container, fg_color="transparent")
        empty_frame.pack(expand=True, pady=60)
        
        ctk.CTkLabel(
            empty_frame,
            text="🛒",
            font=ctk.CTkFont(size=64)
        ).pack(pady=(0, 10))
        
        ctk.CTkLabel(
            empty_frame,
            text="Nenhuma venda hoje",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=Theme.COLORS["text_secondary"]
        ).pack()
        
        ctk.CTkLabel(
            empty_frame,
            text="Abra o PDV para iniciar as vendas",
            font=ctk.CTkFont(size=14),
            text_color=Theme.COLORS["text_secondary"]
        ).pack(pady=(5, 15))
        
        ctk.CTkButton(
            empty_frame,
            text="🛒 Abrir PDV",
            command=self.on_pdv_click,
            fg_color=Theme.COLORS["success"],
            hover_color=Theme.COLORS["success"],
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack()
    
    def _create_sale_item(self, venda):
        """
        Create a sale item widget
        
        Args:
            venda: Sale object
        """
        item = ctk.CTkFrame(self.recent_sales_container, fg_color=Theme.COLORS["bg_hover"], corner_radius=8)
        item.pack(fill="x", pady=2)
        
        # Time
        ctk.CTkLabel(
            item,
            text=venda.data_hora.strftime("%H:%M"),
            font=ctk.CTkFont(size=12, weight="bold"),
            width=60
        ).pack(side="left", padx=10, pady=10)
        
        # Info
        info = ctk.CTkFrame(item, fg_color="transparent")
        info.pack(side="left", fill="both", expand=True)
        
        ctk.CTkLabel(
            info,
            text=f"Venda #{venda.id}",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        ).pack(fill="x")
        
        ctk.CTkLabel(
            info,
            text=f"{venda.forma_pagamento}",
            font=ctk.CTkFont(size=12),
            text_color="gray",
            anchor="w"
        ).pack(fill="x")
        
        # Value
        ctk.CTkLabel(
            item,
            text=f"R$ {venda.total:.2f}",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=Theme.COLORS["success"]
        ).pack(side="right", padx=15)
