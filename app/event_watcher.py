import sched, time, sys
from kubernetes import client, config, watch

#Config varables
TIMER_FREQUENCY_IN_SECONDS=3600
INITIAL_DELAY_IN_SECONDS = 10

#Load K8s cluster configuration
config.load_incluster_config()

#Get api client
v1 = client.CoreV1Api()

#Block to get the pod events
def lookup_pod_events():
    for event in watch.Watch().stream(v1.list_pod_for_all_namespaces, timeout_seconds=10):
           print( "Event: %s %s %s" % ( event["type"],event["object"].kind,event["object"].metadata.name)) 

#Block to get the node events
def lookup_node_events():
    for event in watch.Watch().stream(v1.list_node, timeout_seconds=10):
           print( "Event: %s %s %s" % ( event["type"],event["object"].kind,event["object"].metadata.name)) 
  
#Block to get namespace events
def lookup_ns_events():
    for event in watch.Watch().stream(v1.list_namespace, timeout_seconds=10):
           print( "Event: %s %s %s" % ( event["type"],event["object"].kind,event["object"].metadata.name)) 
  
#Block to get service events
def lookup_service_events():
    for event in watch.Watch().stream(v1.list_service_for_all_namespaces, timeout_seconds=10):
           print( "Event: %s %s %s" % ( event["type"],event["object"].kind,event["object"].metadata.name)) 

#Block to get pvc events
def lookup_pvc_events():
    for event in watch.Watch().stream(v1.list_persistent_volume_claim_for_all_namespaces, timeout_seconds=10):
           print( "Event: %s %s %s" % ( event["type"],event["object"].kind,event["object"].metadata.name)) 


def lookup_events(sc):
    if "pod" in optionsList:
        #Get pod events
        lookup_pod_events()
    if "namespace" in optionsList:
        #Get namespace events
        lookup_ns_events()
    if "node" in optionsList:
        #Get node events
        lookup_node_events()
    if "service" in optionsList:
        #Get service events
        lookup_service_events()
    if "pvc" in optionsList:
        #Get pvc events
        lookup_pvc_events()
    
    #Rinse and repeat       
    s.enter(TIMER_FREQUENCY_IN_SECONDS, 1, lookup_events, (sc,))

    
    
#Start here
if __name__ == '__main__':
    if len(sys.argv) > 1:
        optionsList = sys.argv[1]
        #Initialize the scheduler
        s = sched.scheduler(time.time, time.sleep)
        s.enter(INITIAL_DELAY_IN_SECONDS, 1, lookup_events, (s,))
        s.run()
    else:
        print("Wrong number of arguments!")
        print("Usage: python event_watcher.py [pod,node,namespace,service,pvc]")
