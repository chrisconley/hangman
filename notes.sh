./setup.sh
ami=ami-2511234c
ec2-run-instances $ami \
    --key chrisconley-io \
    --instance-type c3.8xlarge \
    -g default \
    -b /dev/sda=:160:true # true deletes volume on termination

ec2-describe-instances | grep running
ip=54.227.78.5

ssh ubuntu@$ip
# ec2 box
sudo apt-get update
sudo apt-get install build-essential -y

rsync -avt \
  --delete --exclude=".git" --exclude="build" --exclude="venv" \
  . ubuntu@$ip:hangman-python
