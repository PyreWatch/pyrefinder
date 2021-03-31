# Paths

Our MQTT system is split into two paths: one for websockets and standard TCP. The websockets system (port 1884) is to be used for the web application so that live events, such as status, from fighters can be displayed in realtime. The standard connection (port 1883) is to be used to store the information incoming from fighters directly into finder and proper folders to be used for initial loads of the page prior to the connection with websockets and for record purposes. For more information refer to the specfic sections.

## Websockets

The paths to be published/subscribed to are the following:

* `<:area>/device_status/#`: All device statuses are available on subscription, within a given area.
  * requires: {id:str, lat:float, lng:float, json_payload:str}

* `<:area>/device_status/<:device_id>`: A sign device status is available on subscription; a device status should be published using this.
  * For example a device with id "fighter1" in Yosemite Park should be published to: `yosemite/device_status/fighter1`
  * requires: {id:str, lat:float, lng:float, json_payload:{conf:float, status:str}}

* `<:area>/alerts/message`: If there is a fire detected within a given area, an alert message should be sent to the alerts message for subscription; used for notifications.
  * requires: {id:str, lat:float, lng:float, msg:str}

## TCP/Standard MQTT

* `<:area>/device_status/#`: All device statuses are available on subscription, within a given area.
  * requires: {id:str, lat:float, lng:float, json_payload:str}

* `<:area>/device_status/<:device_id>`: A sign device status is available on subscription; a device status should be published using this. For example a device with id "fighter1" in Yosemite Park should be published to: `yosemite/device_status/fighter1`
  * requires: {id:str, lat:float, lng:float, json_payload:{conf:float, status:str}}

* `<:area>/alerts/message`: If there is a fire detected within a given area, an alert message should be sent to the alerts message for subscription; used for notifications.
  * requires: {id:str, lat:float, lng:float, msg:str}
