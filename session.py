from scapy.all import *
from threading import Thread
import sys


class TcpSession:

   def __init__(self,src, target):
      self.seq = 0
      self.ack = 0
      self.ip = IP(src= src, dst=target[0])
      self.sport =  random.randint(1025,65500)
      self.dport = target[1]
      self.connected = False
      self._ackThread = None
      self._timeout = 3
      
   def _ack(self, p):
      self.ack = p[TCP].seq + len(p[Raw])
      ack = self.ip/TCP(sport=self.sport, dport=self.dport, flags='A', seq=self.seq, ack=self.ack)
      send(ack)

   def _ack_rclose(self):
      self.connected = False

      self.ack += 1
      fin_ack = self.ip/TCP(sport=self.sport, dport=self.dport, flags='FA', seq=self.seq, ack=self.ack)
      ack = sr1(fin_ack, timeout=self._timeout)
      self.seq += 1

      assert ack.haslayer(TCP), 'TCP layer missing'
      assert ack[TCP].flags & 0x10 == 0x10 , 'No ACK flag'
      assert ack[TCP].ack == self.seq , 'Acknowledgment number error'
      

   def _sniff(self):
      s = L3RawSocket()
      timeout = time.time() + 10
      while self.connected and time.time() < timeout:
         p = s.recv(MTU)
         if p !=None and p.haslayer(TCP) and p.haslayer(Raw) \
            and p[TCP].dport == self.sport :
	       print p[TCP]
#               print p[TCP][RAW]
               self._ack(p)
         if p.haslayer(TCP) and p[TCP].dport == self.sport \
            and p[TCP].flags & 0x01 == 0x01 : # FIN
               self._ack_rclose()            
      s.close()
      self._ackThread = None
      print('Acknowledgment thread stopped')

   def _start_ackThread(self):
      self._ackThread = Thread(name='AckThread',target=self._sniff)
      self._ackThread.start()

   def connect(self):
      self.seq = random.randrange(0,(2**32)-1)

      syn = self.ip/TCP(sport=self.sport, dport=self.dport, seq=self.seq, flags='S')
      syn_ack = sr1(syn, timeout=self._timeout)
      self.seq += 1
      
      assert syn_ack.haslayer(TCP) , 'TCP layer missing'
      assert syn_ack[TCP].flags & 0x12 == 0x12 , 'No SYN/ACK flags'
      assert syn_ack[TCP].ack == self.seq , 'Acknowledgment number error'

      self.ack = syn_ack[TCP].seq + 1
      ack = self.ip/TCP(sport=self.sport, dport=self.dport, seq=self.seq, flags='A', ack=self.ack)
      send(ack)

      self.connected = True
      self._start_ackThread()
      print('Connected')

   def close(self):
      self.connected = False

      fin = self.ip/TCP(sport=self.sport, dport=self.dport, flags='FA', seq=self.seq, ack=self.ack)
      fin_ack = sr1(fin, timeout=self._timeout)
      self.seq += 1

      assert fin_ack.haslayer(TCP), 'TCP layer missing'
      assert fin_ack[TCP].flags & 0x11 == 0x11 , 'No FIN/ACK flags'
      assert fin_ack[TCP].ack == self.seq , 'Acknowledgment number error'

      self.ack = fin_ack[TCP].seq
      ack = self.ip/TCP(sport=self.sport, dport=self.dport, flags='A', seq=self.seq,  ack=self.ack)
      send(ack)

      print('Disconnected')

   def build(self, payload):
      psh = self.ip/TCP(sport=self.sport, dport=self.dport, flags='PA', seq=self.seq, ack=self.ack)/payload
      self.seq += len(psh[Raw])
      return psh

   def send(self, payload):
      psh = self.build(payload)
      ack = sr(psh, timeout=5)
   #   self.ack = ack[TCP].ack
   #   print ack.summary()
   #   self.seq = self.seq + 1
   #   print ack.summary()
   #   ack = self.ip/TCP(sport=self.sport, dport=self.dport, seq=self.seq, flags='A', ack=self.ack)
   #   result = sr1(ack, timeout=5)
   #   print result.summary()
     # exit
     # assert ack.haslayer(TCP), 'TCP layer missing'
     # assert ack[TCP].flags & 0x10 == 0x10, 'No ACK flag'
     # assert ack[TCP].ack == self.seq , 'Acknowledgment number error'
sess = TcpSession(sys.argv[1], (sys.argv[2], 80))
sess.connect()
sess.send('GET /index.html HTTP/1.1\r\n\r\n')
#sess.close()
