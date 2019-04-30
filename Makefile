deploy:
	scp *.py 192.168.3.4:/opt/zehnder-can-mqtt
ohitems:
	cd openhab && python3 items.py > comofair.items

.PHONY: deploy ohitems
