import xml.etree.ElementTree as ET

def parse_scl(file_path):  # função de extrair informações do arquivo SCL
    # Parse the XML file
    tree = ET.parse(file_path) # carregando o arquivo SCD_model.scd
    root = tree.getroot()   # obtendo a raiz do arquivo XML

    ns = {'scl': 'http://www.iec.ch/61850/2003/SCL'} # cria tags para navegar no XML
    
    ieds = [] # lista para armazenar as informações dos IEDs
    
    for subnetwork in root.findall('scl:Communication/scl:SubNetwork', ns): # navegando até a tag SubNetwork
        subnetwork_name = subnetwork.get('name') # obtendo o nome da subrede
        
        for connected_ap in subnetwork.findall('scl:ConnectedAP', ns): # navegando até a tag ConnectedAP
            ied_name = connected_ap.get('iedName') # obtendo o nome do IED
            ap_name = connected_ap.get('apName') # obtendo o nome do ponto de acesso
            address = connected_ap.find('scl:Address', ns) # navegando até a tag Address
            
            if address is not None: # verificando se a tag Address existe
                ip = address.find('scl:P[@type="IP"]', ns) # obtendo o endereço IP
                subnet = address.find('scl:P[@type="IP-SUBNET"]', ns) # obtendo a máscara de sub-rede
                gateway = address.find('scl:P[@type="IP-GATEWAY"]', ns) # obtendo o gateway
                
                ieds.append({ # armazenando as informações na lista
                    'subnetwork': subnetwork_name, # nome da subrede
                    'ied_name': ied_name,
                    'ap_name': ap_name, # nome do ponto de acesso
                    'ip': ip.text if ip is not None else None,
                    'subnet': subnet.text if subnet is not None else None,
                    'gateway': gateway.text if gateway is not None else None
                })
    
    return ieds # retornando a lista de IEDs com suas informações

if __name__ == "__main__": 
    file_path = '/home/arthur-dev/Desktop/estudos-gêmeosdigitais/Analisador/IEC station 1.scd'
    ied_info = parse_scl(file_path) # chamando a função para extrair as informações do arquivo SCL

    print(f"Número de PCs/IED analisados e retornados:", len(ied_info)) # imprimindo o número de IEDs encontrados

    for ied in ied_info: # imprimindo as informações de cada IED
        print(f"Subnetwork: {ied['subnetwork']}")
        print(f"IED Name: {ied['ied_name']}")
        print(f"Access Point Name: {ied['ap_name']}")
        print(f"IP Address: {ied['ip']}")
        print(f"Subnet Mask: {ied['subnet']}")
        print(f"Gateway: {ied['gateway']}")
        print("-" * 40)
