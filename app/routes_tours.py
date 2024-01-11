from flask import Blueprint, render_template

routes_tours = Blueprint('routes_tours', __name__)


@routes_tours.route('/tours')
def tours():
    return render_template('tours.html')


@routes_tours.route('/tours/lagoverde')
def lagoverde():
    return render_template('tours/lagoverde/lagoverde.html')


@routes_tours.route('/tours/alterdochao')
def alterdochaotour():
    return render_template('tours/lagoverde/alterdochaotour.html')


@routes_tours.route('/tours/florestaencantada')
def florestaencantada():
    return render_template('tours/lagoverde/florestaencantada.html')


@routes_tours.route('/tours/igarapedocamarao')
def igarapedocamarao():
    return render_template('tours/lagoverde/igarapedocamarao.html')


@routes_tours.route('/tours/igarapedomacaco')
def igarapedomacaco():
    return render_template('tours/lagoverde/igarapedomacaco.html')


@routes_tours.route('/tours/pontadavaleria')
def pontadavaleria():
    return render_template('tours/lagoverde/pontadavaleria.html')


@routes_tours.route('/tours/subindoorio/pindobal')
def pindobal():
    return render_template('tours/subindoorio/pindobal.html')


@routes_tours.route('/tours/subindoorio/mureta')
def mureta():
    return render_template('tours/subindoorio/mureta.html')


@routes_tours.route('/tours/subindoorio/jurucui')
def jurucui():
    return render_template('tours/subindoorio/jurucui.html')


@routes_tours.route('/tours/subindoorio/cajutuba')
def cajutuba():
    return render_template('tours/subindoorio/cajutuba.html')


@routes_tours.route('/tours/subindoorio/aramanai')
def aramanai():
    return render_template('tours/subindoorio/aramanai.html')


@routes_tours.route('/tours/rioarapiuns/pontadotorono')
def pontadotorono():
    return render_template('tours/rioarapiuns/pontadotorono.html')


@routes_tours.route('/tours/rioarapiuns/pontagrande')
def pontagrande():
    return render_template('tours/rioarapiuns/pontagrande.html')


@routes_tours.route('/tours/rioarapiuns/meliponario')
def meliponario():
    return render_template('tours/rioarapiuns/meliponario.html')


@routes_tours.route('/tours/rioarapiuns/icuxi')
def icuxi():
    return render_template('tours/rioarapiuns/icuxi.html')


@routes_tours.route('/tours/rioarapiuns/comunidadecoroca')
def comunidadecoroca():
    return render_template('tours/rioarapiuns/comunidadecoroca.html')


@routes_tours.route('/tours/descendoorio/pontadocururu')
def pontadocururu():
    return render_template('tours/descendoorio/pontadocururu.html')


@routes_tours.route('/tours/descendoorio/pontadepedras')
def pontadepedras():
    return render_template('tours/descendoorio/pontadepedras.html')


@routes_tours.route('/tours/descendoorio/pedradamoca')
def pedradamoca():
    return render_template('tours/descendoorio/pedradamoca.html')


@routes_tours.route('/tours/descendoorio/lagopreto')
def lagopreto():
    return render_template('tours/descendoorio/lagopreto.html')


@routes_tours.route('/tours/descendoorio/lagodojacare')
def lagodojacare():
    return render_template('tours/descendoorio/lagodojacare.html')


@routes_tours.route('/tours/descendoorio/encontrodasaguas')
def encontrodasaguas():
    return render_template('tours/descendoorio/encontrodasaguas.html')


@routes_tours.route('/tours/descendoorio/casadosaulo')
def casadosaulo():
    return render_template('tours/descendoorio/casadosaulo.html')


@routes_tours.route('/tours/descendoorio/canaldojari')
def canaldojari():
    return render_template('tours/descendoorio/canaldojari.html')


@routes_tours.route('/pacotes/passeiocustomizado')
def passeiocustomizado():
    return render_template('pacotes/passeiocustomizado.html')


@routes_tours.route('/pacotes/passeioscomroteirosdefinidos')
def passeioscomroteirosdefinidos():
    return render_template('pacotes/passeioscomroteirosdefinidos.html')


@routes_tours.route('/pacotes/passeiosnorturnosgastronomicos')
def passeiosnorturnosgastronomicos():
    return render_template('pacotes/passeiosnorturnosgastronomicos.html')
