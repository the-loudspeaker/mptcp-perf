# MPTCP Connection performance.

Basic idea is to get the combined bandwidth of all subflows by sending packets of 1KB data
multiple times through a connection and timing it.

appconf.py sets up some MPTCP parameters and functions used in the main scripts.
