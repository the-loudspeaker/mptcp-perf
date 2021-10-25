from subprocess import Popen, PIPE

# IP address and port number of server
server_ip = "172.16.34.21"
server_port = 5000

#  it is possible to create multiple subflows for each pair of IP-addresses.
num_subflows = 2
num_subflows_path = "/sys/module/mptcp_fullmesh/parameters/num_subflows"

scheduler_value = "redundant"
scheduler_key = "net.mptcp.mptcp_scheduler"

pathman_value = "fullmesh"
pathman_key = "net.mptcp.mptcp_path_manager"

# Enable MPTCP
enable_value = 1
enable_key = "net.mptcp.mptcp_enabled"

# This file must be 1KB size.
send_data = "data.bin"
KBYTE = 1024

# Set schedulers and subflows.
def setMptcp():
	writeFile(num_subflows_path, str(num_subflows))
	sysCtl(scheduler_key, scheduler_value)


def writeFile(path, data):
	fo = open(path, "w")
	print ("write " + data + " to " + path)
	fo.write(data)
	fo.close()


def sysCtl(key, value):
  p = Popen("sysctl -w %s=%s" % (key, value), shell=True, stdout=PIPE, stderr=PIPE)
  stdout, stderr = p.communicate()
  print ("stdout=",stdout,"stderr=", stderr)


#Return the given bytes as a human friendly KB, MB, GB, or TB string
def humanbytes(B):
   B = float(B)
   KB = float(KBYTE)
   MB = float(KB ** 2) # 1,048,576
   GB = float(KB ** 3) # 1,073,741,824
   TB = float(KB ** 4) # 1,099,511,627,776

   if B < KB:
      return '{0} {1}'.format(B,'Bytes' if 0 == B > 1 else 'Byte')
   elif KB <= B < MB:
      return '{0:.2f} KB'.format(B/KB)
   elif MB <= B < GB:
      return '{0:.2f} MB'.format(B/MB)
   elif GB <= B < TB:
      return '{0:.2f} GB'.format(B/GB)
   elif TB <= B:
      return '{0:.2f} TB'.format(B/TB)


def kbytes(humanstr):
	sizestr, unit = splitSizestr(humanstr)
	size = int(sizestr)

	if unit == "G" :
		size = size * (KBYTE ** 2)
	elif unit == "M" :
		size = size * (KBYTE)

	return size

def splitSizestr(humanstr):
	upperHumanstr = humanstr.upper()
	sizestr = ""
	unit = ""

	for c in humanstr:
		if c.isdigit():
			sizestr = sizestr + c
		else:
			unit = c
			break

	return sizestr, unit

