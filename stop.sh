kill -9 $(ps aux | grep 'camping_reservation' | awk '{print $2}')
echo "camping_reservation stop..."