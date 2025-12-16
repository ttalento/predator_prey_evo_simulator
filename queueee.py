class queueee:

    def __init__(self):
        self.list = []
        
    def empty_Q(self):
        return self.list==[]

    def next_event(self):
        if (self.empty_Q()):
            print("empty queue")
            return None
        else:
            return self.list[0]

    def add_event(self, id, event_time, event_type):
        event = {'ID': id, 'Time': event_time, 'Type': event_type}
        if (self.empty_Q()):
            self.list = [event]
        elif (event_time>self.list[-1]['Time']):
            self.list += [event]
        else:
            i = 0
            while (event_time > self.list[i]['Time']):
                i+=1
            self.list = self.list[:i] + [event] + self.list[i:]
        
    def Q_size(self):
        return len(self.list)
    
    def pop(self):
        if (self.empty_Q()):
            print("empty queue")
            return None
        else:
            next_event = self.list[0]
            self.list = self.list[1:]
        return next_event
    
    def check_ID_events(self, id):
        res = []
        for event in self.list:
            if(event['ID']==id):
                res += [event]
        return res
    
    def remove_events_by_ID(self, id):
        for i in range(len(self.list)-1,-1,-1):
            event = self.list[i]
            if(event['ID']==id):
                self.list = self.list[:i]+self.list[i+1:]
