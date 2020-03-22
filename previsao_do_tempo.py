import requests
import xml.dom.minidom

class PrevisaoDoTempo:

	def __init__( self, nome_da_cidade ):
		self.previsao = ""
		self.nome_da_cidade = nome_da_cidade

	def obter_codigo_da_cidade( self ):

		retorno_requisicao = requests.get( "http://servicos.cptec.inpe.br/XML/listaCidades", { "city":  self.nome_da_cidade } )
		
		if retorno_requisicao.status_code == 200:

			IF not "<id>" in retorno_requisicao.text:
				print( "Nome da cidade nao encontrado!" )
				return None

			documento_xml = xml.dom.minidom.parseString( retorno_requisicao.text )

			codigo_da_cidade = documento_xml.getElementsByTagName("id")[0].firstChild.data

			return codigo_da_cidade

	def obter_previsao_por_cidade( self ):

		codigo_da_cidade = self.obter_codigo_da_cidade()

		IF codigo_da_cidade:

			retorno_requisicao = requests.get( "http://servicos.cptec.inpe.br/XML/cidade/7dias/" + codigo_da_cidade + "/previsao.xml" )

			return xml.dom.minidom.parseString( retorno_requisicao.text )


	def exibir_previsao_por_cidade( nome_da_cidade ) CLASS previsao_do_tempo:

		LOCAL previsao_xml := ::obter_previsao_por_cidade( nome_da_cidade )
		LOCAL xml_dom := win_OleCreateObject( "MSXML2.DOMDocument.6.0" )
		LOCAL cidade, uf, atualizacao, lista_de_previsoes, previsao, previsao_filhos, elemento
		LOCAL cabecalho := "|", tupla := "|"

		IF !Empty( previsao_xml )

			xml_dom:loadXML( previsao_xml )
			cidade := xml_dom:selectSingleNode( "//nome" ):text
			uf := xml_dom:selectSingleNode( "//uf" ):text
			atualizacao := xml_dom:selectSingleNode( "//atualizacao" ):text

			? "Previsao do tempo para " + cidade + " - " + uf
			? "Atualizada em " + DToC( SToD( StrTran( atualizacao, "-" ) ) )
			?

			lista_de_previsoes := xml_dom:getElementsByTagName( "previsao" )

			FOR EACH elemento IN lista_de_previsoes:item(0):childNodes
				IF elemento:tagName $ "dia"
					cabecalho += PadC(elemento:tagName, 12 ) + "|"
				ELSEIF elemento:tagName $ "tempo"
					cabecalho += PadC(elemento:tagName, 36 ) + "|"
				ELSE
					cabecalho += PadC(elemento:tagName, 8 ) + "|"
				ENDIF
			NEXT
			? "+" + Replicate("-",76) + "+"
			? cabecalho
			? "|" + Replicate("-",12) + "|" + Replicate("-",36) + "|" + Replicate("-",8) + "|" + Replicate("-",8) + "|" + Replicate("-",8) + "|"

			FOR EACH previsao IN lista_de_previsoes
				IF previsao:hasChildNodes()
					previsao_filhos := previsao:childNodes
					FOR EACH elemento IN previsao_filhos
						IF elemento:tagName $ "dia"
							tupla += PadC( DToC( SToD( StrTran( elemento:text, "-" ) ) ), 12 ) + "|"
						ELSEIF elemento:tagName $ "tempo"
							tupla += PadC( ::converter_sigla_em_previsao( elemento:text ), 36 ) + "|"
						ELSE
							tupla += PadC( elemento:text, 8 ) + "|"
						ENDIF
					NEXT
					? tupla
					? "|" + Replicate("-",12) + "|" + Replicate("-",36) + "|" + Replicate("-",8) + "|" + Replicate("-",8) + "|" + Replicate("-",8) + "|"
					tupla := "|"
				ENDIF
			NEXT
		ENDIF

METHOD converter_sigla_em_previsao( sigla ) CLASS previsao_do_tempo

	LOCAL previsao

	SWITCH sigla
		CASE "ec"
			previsao := "Encoberto com Chuvas Isoladas"
			EXIT
		CASE "ci"
			previsao := "Chuvas Isoladas"
			EXIT
		CASE "c"
			previsao := "Chuva"
			EXIT
		CASE "in"
			previsao := "Instável"
			EXIT
		CASE "pp"
			previsao := "Poss. de Pancadas de Chuva"
			EXIT
		CASE "cm"
			previsao := "Chuva pela Manha"
			EXIT
		CASE "cn"
			previsao := "Chuva a Noite"
			EXIT
		CASE "pt"
			previsao := "Pancadas de Chuva a Tarde"
			EXIT
		CASE "pm"
			previsao := "Pancadas de Chuva pela Manha"
			EXIT
		CASE "np"
			previsao := "Nublado e Pancadas de Chuva"
			EXIT
		CASE "pc"
			previsao := "Pancadas de Chuva"
			EXIT
		CASE "pn"
			previsao := "Parcialmente Nublado"
			EXIT
		CASE "cv"
			previsao := "Chuvisco"
			EXIT
		CASE "ch"
			previsao := "Chuvoso"
			EXIT
		CASE "t"
			previsao := "Tempestade"
			EXIT
		CASE "ps"
			previsao := "Predominio de Sol"
			EXIT
		CASE "e"
			previsao := "Encoberto"
			EXIT
		CASE "n"
			previsao := "Nublado"
			EXIT
		CASE "cl"
			previsao := "Ceu Claro"
			EXIT
		CASE "nv"
			previsao := "Nevoeiro"
			EXIT
		CASE "g"
			previsao := "Geada"
			EXIT
		CASE "ne"
			previsao := "Neve"
			EXIT
		CASE "nd"
			previsao := "Nao Definido"
			EXIT
		CASE "pnt"
			previsao := "Pancadas de Chuva a Noite"
			EXIT
		CASE "psc"
			previsao := "Possibilidade de Chuva"
			EXIT
		CASE "pcm"
			previsao := "Possibilidade de Chuva pela Manha"
			EXIT
		CASE "pct"
			previsao := "Possibilidade de Chuva a Tarde"
			EXIT
		CASE "pcn"
			previsao := "Possibilidade de Chuva a Noite"
			EXIT
		CASE "npt"
			previsao := "Nublado com Pancadas a Tarde"
			EXIT
		CASE "npn"
			previsao := "Nublado com Pancadas a Noite"
			EXIT
		CASE "ncn"
			previsao := "Nublado com Poss. de Chuva a Noite"
			EXIT
		CASE "nct"
			previsao := "Nublado com Poss. de Chuva a Tarde"
			EXIT
		CASE "ncm"
			previsao := "Nubl. c/ Poss. de Chuva pela Manha"
			EXIT
		CASE "npm"
			previsao := "Nublado com Pancadas pela Manha"
			EXIT
		CASE "npp"
			previsao := "Nublado com Possibilidade de Chuva"
			EXIT
		CASE "vn"
			previsao := "Variação de Nebulosidade"
			EXIT
		CASE "ct"
			previsao := "Chuva a Tarde"
			EXIT
		CASE "ppn"
			previsao := "Poss. de Panc. de Chuva a Noite"
			EXIT
		CASE "ppt"
			previsao := "Poss. de Panc. de Chuva a Tarde"
			EXIT
		CASE "ppm"
			previsao := "Poss. de Panc. de Chuva pela Manha"
	ENDSWITCH

RETURN previsao