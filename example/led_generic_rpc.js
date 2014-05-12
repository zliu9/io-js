var GA = require('../lib/');

var io = GA.IO_rpc;

io.config({
  'log': true,
  'hostname': 'zliu9-desk5.bj.intel.com',
  'port': 2000
});

io.initWithTty(new Buffer("/dev/tty1"),
               new Buffer("/dev/tty1"),
               new Buffer("/dev/tty1"));

var led = new GA.Led({
  io: io,
  pin: 13
});

led.blink();
