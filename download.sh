

FILE=/home/user/Desktop/projet_m1/output.mp3
DESTINATION=CCI-DIGITAL-MBP05@192.168.1.103:~/Desktop/
PASSWORD=digital

if [ -f "$FILE" ]; then
    sshpass -p $PASSWORD scp $FILE $DESTINATION
    # Optionnel : Supprimer ou déplacer le fichier après le transfert
    rm $FILE
fi
