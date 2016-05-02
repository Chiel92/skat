
<<<"Starting chuck server">>>;
<<<now>>>;

OscRecv orec;
5005 => orec.port;
orec.listen();
orec.event("/frequency,f") @=> OscEvent e;
//orec.event("/debug") @=> OscEvent e;

<<<"Listening for OSC events">>>;

SinOsc s => dac;
300 => s.freq;

while (true)
{
e => now;
<<<"Received at ">>>;
<<<now/1::second>>>;
e.nextMsg();
e.getFloat() => s.freq;
}


