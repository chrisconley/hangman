./setup.sh
ami=ami-2511234c
ec2-run-instances $ami --key ec2-dklr --group dklr --instance-type c3.8xlarge -z us-east-1d -b /dev/sda=:160:true
ec2-describe-instances
ip=54.227.64.184

ssh ubuntu@$ip
# ec2 box
sudo apt-get update
sudo apt-get install build-essential -y

rsync -avt -e "ssh -i /Users/chrisconley/.ssh/ec2-dklr.pem" \
  --delete --exclude=".git" --exclude="build" --exclude="venv" \
  . ubuntu@$ip:
