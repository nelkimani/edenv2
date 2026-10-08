/* Eden settings for receipt.js */
NotifyReceipt.config.shop={
  name:'EDEN ELECTRONICS CHUKA',
  lines:['We care for your home','Chuka Town, Tharaka-Nithi','Tel: 0798928060'],
  footer:['Thank you for shopping with us!','We care for your home']
};
NotifyReceipt.config.paperMm=58;   // P58E roll
NotifyReceipt.config.cols=32;      // 58mm = 32 characters per line
NotifyReceipt.config.bleChunk=20;  // safe Bluetooth write size; raise to 100 if your printer is fine with it
NotifyReceipt.config.cut=false;     // small 58mm printers have no cutter: just feed the paper (set true if yours cuts)
