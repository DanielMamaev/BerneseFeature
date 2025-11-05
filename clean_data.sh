#!/bin/sh

usage() {
    echo "Использование: $0 [CAMPAIGN|SAVEDISK|DATAPOOL|ALL]"
    exit 1
}

[ $# -eq 0 ] && usage

while [ $# -gt 0 ]; do
    case "$1" in
        CAMPAIGN)
            echo "Чищу CAMPAIGN52..."
            rm -r "${P}/EXAMPLE/ATM/"* \
                  "${P}/EXAMPLE/BPE/"* \
                  "${P}/EXAMPLE/GRD/"* \
                  "${P}/EXAMPLE/MSC/"* \
                  "${P}/EXAMPLE/OBS/"* \
                  "${P}/EXAMPLE/ORB/"* \
                  "${P}/EXAMPLE/ORX/"* \
                  "${P}/EXAMPLE/OUT/"* \
                  "${P}/EXAMPLE/RAW/"* \
                  "${P}/EXAMPLE/SOL/"*
            cd "${P}/EXAMPLE/STA/" || exit 1
            find . -mindepth 1 -maxdepth 1 ! -name 'SESSIONS.SES' -exec rm -rf {} +
            rm -f "${D}/REF52/EXAMPLE.CRD" "${D}/REF52/EXAMPLE.VEL"
            ;;
        SAVEDISK)
            echo "Чищу SAVEDISK..."
            rm -r "${S}/PPP/"* \
                  "${S}/RNX2SNX/"*
            ;;
        DATAPOOL)
            echo "Чищу DATAPOOL..."
            rm -r "${D}/BSW52/"* \
                  "${D}/COD/"* \
                  "${D}/COM/"* \
                  "${D}/HOURLY/"* \
                  "${D}/IGS/"* \
                  "${D}/LEO/"* \
                  "${D}/MSC/"* \
                  "${D}/REF52/"* \
                  "${D}/RINEX/"* \
                  "${D}/RINEX3/"* \
                  "${D}/SLR_NP/"* \
                  "${D}/STAT_LOG/"* \
                  "${D}/VMF1/"*
            ;;
        ALL)
            echo "Удаляю всё..."
            "$0" CAMPAIGN
            "$0" SAVEDISK
            "$0" DATAPOOL
            ;;
        *)
            echo "Неизвестный аргумент: $1"
            usage
            ;;
    esac
    shift
done
