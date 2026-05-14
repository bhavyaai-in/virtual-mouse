
1. Naya Tunnel Create karo (Naam: mouse)
Bash
cloudflared tunnel create mouse
(Isse tumhe ek nayi ID milegi, use dekh lena).

2. Subdomain Route set karo
Purana q ya mouse ka koi bhi purana DNS record ho, ye use overwrite kar dega:

Bash
cloudflared tunnel route dns mouse mouse
(Iska matlab: mouse naam ki tunnel ko desired subdomain par bhej do).

3. Tunnel Run karo
Bash
cloudflared tunnel run --url http://localhost:8765 mouse



cloudflared tunnel run --url http://localhost:8765 mouse




cloudflared tunnel create ollama

cloudflared tunnel route dns ollama 8Kz2nP9vL4mX7qR1

cloudflared tunnel run --url http://localhost:8765 ollama


https://8kz2np9vl4mx7qr1.bhavyaai.com/


nano ~/.continue/config.yaml

models:
  - name: Codestral Autocomplete
    provider: ollama
    model: codestral
    apiBase: https://8kz2np9vl4mx7qr1.bhavyaai.com
    roles:
      - autocomplete