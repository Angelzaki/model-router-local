<div align="center">

# model-router-local

**Router cheap / strong / abstain** · Angel Salazar

<br/>
<img src="docs/diagram.jpg" alt="Problema → Solución → Resultado" width="100%"/>

</div>

---

### `$ cat diagrama.md`

```mermaid
flowchart LR
  P[Problema<br/>Todo va al modelo caro] --> S[Solución<br/>Router cheap / strong / abstain]
  S --> R[Resultado<br/>Ahorro sin perder calidad en lo simple]
```

---

### `$ cat problema.md`

Mandar todo a Sonnet/Opus sale caro.  
Clasificamos la query y elegimos modelo (o abstenerse).

---

```bash
pip install -e .
pytest
python -m model_router route "¿Cuál es el límite comercial?"
python -m model_router bench
```

---

Hecho en Lima · Angel Salazar · CIP 404730
