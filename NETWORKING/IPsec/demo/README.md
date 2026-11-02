# IPsec VPN demo

A local map of one HR request. The packet moves from the café laptop, through the hotel, into the office gateway, and on to HR. Nothing here opens a real tunnel.

## Run it

```bash
cd NETWORKING/IPsec/demo
python3 server.py
```

Open the address it prints, usually http://127.0.0.1:8765

## What to click

1. **Guided tour.** Ten short steps. Next, or Play all. Click a blue term if you want the one-line meaning.
2. **Try a scenario.** Change the place, the product, and the password, then send the request. Read the headline the backend returns.
3. **All terms.** The same words the tour uses, in one list.

Try these three scenarios after the tour:

| Place | Product | Password | What you should see |
| --- | --- | --- | --- |
| Home | IPsec VPN | Correct | Connected with ESP inside UDP 4500 |
| Hotel | IPsec VPN | Correct | UDP blocked, then SSL VPN on TCP 443 |
| Home | IPsec VPN | Wrong | Login fails, and it does not fall back |
