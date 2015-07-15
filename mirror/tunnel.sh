# Runs on NUC
while test 1
do
date
echo opening ssh telemetry tunnel to ISP
ssh user@internet.example.org -R 8081:localhost:8080 -N
sleep 5
done

