#!/bin/bash
name=$(echo $1 | awk -F "/" '{print $3}')
echo -e "URL: $1" > output/url/$name.url.report
function getURLInfo(){
curl -s --request POST --url https://www.virustotal.com/api/v3/urls --header 'x-apikey: XXXX' --form url=$1 > result1
id=$(cat result1 | jq | grep id | awk -F "\"" '{print $4}')
rm result1
curl -s --request GET --url https://www.virustotal.com/api/v3/analyses/$id --header 'x-apikey: XXXX' > result2
outcome=$(cat result2 | grep -E "harmless|undetected" | grep -v 0 | wc -l)
if [[ $outcome -eq 0 ]] ; then echo -e "[i] API call failed, trying again. Be patient."; sleep 4 ; getURLInfo "$1" ; fi
}
getURLInfo "$1"
echo -e "\nAccording to VirusTotal API:"  >> output/url/$name.url.report
cat result2 | jq | grep -E "harmless|malicious|suspicious|undetected" | grep -iEv "Result|category" | tr -d "\"" | sed 's/\<\([[:lower:]]\)\([[:alnum:]]*\)/\u\1\2/g' | tr -d "," >> output/url/$name.url.report
malicious_sources=$(cat result2 | grep malicious -B 2 | grep -v malicious | grep -E "[[:alpha:]]" | grep -vE "stats|harmless" | tr -d "\":{")
if [ ! -z "$malicious_sources" ];
then echo -e "\nThe following sources says that the URL is malicious:\n" >> output/url/$name.url.report
        for i in $(echo $malicious_sources)
        do
                echo -e "$i - $(cat result2| grep $i -A 2  | grep result | tr -d '\",' | awk '{print $2}')" >> output/url/$name.url.report
        done
else 
echo -e "\nThe URL is safe to use!" >> output/url/$name.url.report
fi
cat output/url/$name.url.report >> output/url/url.master.report
echo -e "\n" >> output/url/url.master.report
rm result2
