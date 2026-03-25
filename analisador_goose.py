from scapy.all import rdpcap, Ether

PCAP_FILE = "captura.pcap"

# Liste aqui os MACs REAIS dos seus IEDs autorizados
IEDS_AUTORIZADOS = {
    "02:42:2f:6f:5c:00",
    "02:42:ea:5b:45:00",
    "02:42:64:c1:62:00", 
    "02:42:44:88:27:00", 
    "02:42:61:1f:7f:00",
}

GOOSE_ETHERTYPE = 0x88B8


def analisar_goose(pcap_file: str) -> None:
    try:
        pacotes = rdpcap(pcap_file)
    except FileNotFoundError:
        print(f"Erro: arquivo '{pcap_file}' não encontrado.")
        return
    except Exception as exc:
        print(f"Erro ao abrir o PCAP: {exc}")
        return

    total_goose = 0
    alertas = []

    for i, pkt in enumerate(pacotes, start=1):
        if not pkt.haslayer(Ether):
            continue

        eth = pkt[Ether]

        if eth.type != GOOSE_ETHERTYPE:
            continue

        total_goose += 1
        src_mac = eth.src.lower()
        dst_mac = eth.dst.lower()

        if src_mac not in IEDS_AUTORIZADOS:
            alertas.append({
                "pacote": i,
                "src_mac": src_mac,
                "dst_mac": dst_mac,
                "tamanho": len(pkt),
            })

    print("===== RELATÓRIO DE ANÁLISE GOOSE =====")
    print(f"Arquivo analisado: {pcap_file}")
    print(f"Total de pacotes GOOSE: {total_goose}")
    print(f"Total de alertas: {len(alertas)}")

    if not alertas:
        print("\nNenhuma anomalia detectada.")
        return

    print("\n===== ALERTAS =====")
    for alerta in alertas:
        print(
            f"Pacote {alerta['pacote']} | "
            f"Origem não autorizada: {alerta['src_mac']} | "
            f"Destino: {alerta['dst_mac']} | "
            f"Tamanho: {alerta['tamanho']} bytes"
        )


if __name__ == "__main__":
    analisar_goose(PCAP_FILE)
