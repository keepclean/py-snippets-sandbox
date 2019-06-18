import xml.etree.ElementTree as ET

service_types = {
    "0": "filesystem",
    "1": "directory",
    "2": "file",
    "3": "program with pidfile",
    "4": "remote host",
    "5": "system",
    "6": "fifo",
    "7": "program with path",
    "8": "network",
}

with open('monit-status.xml') as f:
    tree = ET.parse(f)
    root = tree.getroot()

    for service in root.findall('service'):
        print(
            service_types[service.get('type')],
            service.find('name').text,
            service.find('status').text,
            service.find('status_hint').text,
            service.find('monitor').text,
            service.findtext('program/status', ""),
        )
