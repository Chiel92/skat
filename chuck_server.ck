
<<<"Starting chuck server">>>;

OscRecv orec;
5005 => orec.port;
orec.listen();
orec.event("/frequency,f,f") @=> OscEvent e;
//orec.event("/debug") @=> OscEvent e;

<<<"Listening for OSC events">>>;

SinOsc s1 => dac;
SinOsc s2 => dac;
SinOsc s3 => dac;
100 => s1.freq;
100 => s2.sfreq;
100 => s3.sfreq;

while (true)
{
e => now;
<<<"Received at ">>>;
e.nextMsg();
e.getFloat() => s1.freq;
e.getFloat() => s2.sfreq;
e.getFloat() => s3.sfreq;
//s.pluck(0);
//s.noteOn(1);
}


