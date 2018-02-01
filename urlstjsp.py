dic_urls = {
        '1':{
            'url': "http://esaj.tjsp.jus.br/cjpg/pesquisar.do?conversationId=&dadosConsulta.pesquisaLivre=&tipoNumero=UNIFICADO&numeroDigitoAnoUnificado=&foroNumeroUnificado=&dadosConsulta.nuProcesso=&dadosConsulta.nuProcessoAntigo=&classeTreeSelection.values=&classeTreeSelection.text=&assuntoTreeSelection.values=&assuntoTreeSelection.text=&agenteSelectedEntitiesList=&contadoragente=0&contadorMaioragente=0&cdAgente=&nmAgente=&dadosConsulta.dtInicio=&dadosConsulta.dtFim=&varasTreeSelection.values=81-3%2C81-4%2C81-2%2C81-1&varasTreeSelection.text=4+Registros+selecionados&dadosConsulta.ordenacao=DESC",
            'pagin': 1,
            'nr_registros': 16398,
            'done': False
        }
}

def nr_paginas(nr_regs):
    return int(nr_regs/15)