import json
import requests
import hashlib
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app= Flask(__name__)

@app.route('/<string:PhoneNumber>')
def CoWinGetOTP(PhoneNumber):
    print(PhoneNumber)
    msg= request.form.get('Body')
    Generate_OTP_url= "https://cdn-api.co-vin.in/api/v2/auth/generateMobileOTP"
    payload="{\r\n    \"mobile\": \""+str(PhoneNumber)+"\",\r\n    \"secret\": \"U2FsdGVkX1/otFX50SCuGDioac5Zv4Ge9sQm+Lzzkv4vCFz9XiJ1YSfItqueTEMHn4T8viiZrpsj1goFjF6YEg==\"\r\n}"
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url= Generate_OTP_url , headers=headers, data=payload)
    respose_code= response.status_code
    if (respose_code is not 200):
        print(str(respose_code))    
    response_json=response.json()
    print(response_json["txnId"])
    txnId= str(response_json["txnId"])
    print("%%%%%%%%%%%%%%")
    OTP= GetOtp()
    BearerToken=ConfirmOTP(OTP, txnId)
    print(BearerToken)


def GetOtp():
    OTP= input("OTP :")
    return(OTP)

def ConfirmOTP(OTP, txnId):    
    #print("TXN ID: "+txnId)
    hashed_output= hashlib.sha256(OTP.encode('ascii')).hexdigest()
    print(hashed_output)

    confirm_otp_url= "https://cdn-api.co-vin.in/api/v2/auth/validateMobileOtp"

    data="{\r\n    \"otp\": \""+str(hashed_output)+"\",\r\n    \"txnId\": \""+str(txnId)+"\"\r\n}"
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url= confirm_otp_url , headers=headers, data=data)
    print(response.text)
    response_json= response.json()
    token= response_json["token"]
    return(token)
    # resp.message("You said: {}".format(msg))
    # return str(resp)

if __name__== "__main__":
    app.run(debug=True)



