import streamlit as st
import paho.mqtt.client as mqtt


st.title("Esp32 MQTT Dashboard")
st.subheader("Belajar Esp32 Dashboard")
data1 = [0]
data2 = [0]
placeholder = st.empty()
button1,button2 = st.columns(2)
col1,col2 = st.columns(2)
#funsi untuk MQTT
def on_connect(client,userdata,flags,rc):
    col1.success("Subcribe to "+subcribeTopic1)
    col2.success("Subcribe to "+subcribeTopic2)
def on_disconnect(client,userdata,flags,rc):
    st.write("Disconnected")
def get_mqtt_client():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    return client
def on_publish(client,userdata,mid):
    print("mid "+ str(mid))
def on_message(client,userdata,msg):
    if msg.topic == "test/latihan/tempC":
        data1.append(msg.payload.decode("utf-8"))
    elif msg.topic == "test/latihan/humid":
        data2.append(msg.payload.decode("utf-8"))
    with placeholder.container():
        col1,col2 = st.columns(2)
        suhu = "{} C".format(data1[-1])
        humid = "{} %".format(data2[-1])
        col1.metric(label="Suhu", value=suhu)
        col2.metric(label="kelembapan",value=humid)
broker = "mqtt.ardumeka.com"
port = 11219
publishTopic = "latihanIoT112233"
subcribeTopic1 = "test/latihan/tempC"
subcribeTopic2 = "test/latihan/humid"
client = get_mqtt_client()
client.on_publish = on_publish
client.connect(broker,int(port),60)

if button1.button("Klik saya"):
    client.publish(publishTopic,"Lampu ON")
run = False
if button2.button("run monitoring"):
    if run:
        run = False
    else:
        run = True
print(run)
while run:
    client = get_mqtt_client()
    client.connect(broker,port,60)
    client.on_message = on_message
    client.subscribe([(subcribeTopic1,0),(subcribeTopic2,0)])
    client.loop_forever()
