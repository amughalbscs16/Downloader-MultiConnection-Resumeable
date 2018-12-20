# Multiple Connections TCP/UDP Downloaded
	HTTP Didn't Allow UDP so the implementation is not Added.
	As far as TCP is concerned the project comes up with the following features
# Features of Project
	Download Http File from Online/Local Resource
	Download using single TCP Connections
	Download using multiple TCP Connections
	Download resumes on both single/multiple Connections Downloads

# Running the Project
	client.py -r -n <num_connections> -i <metric_interval> -c <connection_type> -f
	<file_location> -o <output_location>
	-n (Required) Total number of simultaneous connections
	-i (Required) Time interval in seconds between metric reporting
	-c (Required) Type of connection: UDP or TCP
	-f (Required) Address pointing to the file location on the web
	-o (Required) Address pointing to the location where the file is downloaded
	-r (Required) Whether to resume the existing download in progress
	As an example, if you want to download a file in current directory (denoted by „.‟) using 8
	simultaneous connections located at http://www.example.com/myfile.png using TCP and rep

# Example
	client.py -n 8 -i 0.5 -c TCP -f http://www.example.com/myfile.png -o .
