# Podział podsieci – 192.168.100.0/23

## Założenia

Sieć: **192.168.100.0/23**

### Działy i zapotrzebowanie

| Dział        | Hosty |
| ------------ | ----- |
| Laboratorium | 70    |
| Biuro        | 30    |
| Magazyn      | 20    |
| HR           | 12    |
| Monitoring   | 6     |

## Over-provisioning

(+50% +1 router)

| Dział        | Wymagane hosty |
| ------------ | -------------- |
| Laboratorium | 106            |
| Biuro        | 46             |
| Magazyn      | 31             |
| HR           | 19             |
| Monitoring   | 10             |

## Dobór podsieci

| Dział        | Maska | Liczba hostów |
| ------------ | ----- | ------------- |
| Laboratorium | /25   | 126           |
| Biuro        | /26   | 62            |
| Magazyn      | /26   | 62            |
| HR           | /27   | 30            |
| Monitoring   | /28   | 14            |

# Rozwiązanie (drzewko)

## Wersja 1 (z nieużywanymi podsieciami)

```
192.168.100.0/23:
	- 192.168.100.0/24:
		- 192.168.100.0/25 (LABORATORIUM, 126)
		- 192.168.100.128/25:
			- 192.168.100.128/26 (BIURO, 62)
			- 192.168.100.192/26 (MAGAZYN, 62)
	- 192.168.101.0/24:
		- 192.168.101.0/25:
			- 192.168.101.0/26:
				- 192.168.101.0/27 (HR, 30)
				- 192.168.101.32/27:
					- 192.168.101.32/28 (MONITORING, 14)
					- 192.168.101.48/28 (unused, 14)
			- 192.168.101.64/26 (unused, 62)
		- 192.168.101.128/25 (unused, 126)
```

## Wersja 2 (wszystkie adresy wykorzystane)

```
192.168.100.0/23:
	- 192.168.100.0/24:
		- 192.168.100.0/25 (LABORATORIUM, 126)
		- 192.168.100.128/25:
			- 192.168.100.128/26 (BIURO, 62)
			- 192.168.100.192/26 (MAGAZYN, 62)
	- 192.168.101.0/24:
		- 192.168.101.0/25:
			- 192.168.101.0/26 (HR + MONITORING, 62)
			- 192.168.101.64/26 (REZERWA, 62)
		- 192.168.101.128/25 (REZERWA, 126)
```

# Lista podsieci

## LABORATORIUM (192.168.100.0/25)

* adres podsieci: 192.168.100.0
* pierwszy host: 192.168.100.1
* ostatni host: 192.168.100.126
* broadcast: 192.168.100.127
* liczba hostów: 126

**Nadwyżka:**

* względem minimalnej (70): +56
* względem over-provisioningu (106): +20

## BIURO (192.168.100.128/26)

* adres podsieci: 192.168.100.128
* pierwszy host: 192.168.100.129
* ostatni host: 192.168.100.190
* broadcast: 192.168.100.191
* liczba hostów: 62

**Nadwyżka:**

* względem minimalnej (30): +32
* względem over-provisioningu (46): +16

## MAGAZYN (192.168.100.192/26)

* adres podsieci: 192.168.100.192
* pierwszy host: 192.168.100.193
* ostatni host: 192.168.100.254
* broadcast: 192.168.100.255
* liczba hostów: 62

**Nadwyżka:**

* względem minimalnej (20): +42
* względem over-provisioningu (31): +31

## HR (192.168.101.0/27)

* adres podsieci: 192.168.101.0
* pierwszy host: 192.168.101.1
* ostatni host: 192.168.101.30
* broadcast: 192.168.101.31
* liczba hostów: 30

**Nadwyżka:**

* względem minimalnej (12): +18
* względem over-provisioningu (19): +11

## MONITORING (192.168.101.32/28)

* adres podsieci: 192.168.101.32
* pierwszy host: 192.168.101.33
* ostatni host: 192.168.101.46
* broadcast: 192.168.101.47
* liczba hostów: 14

**Nadwyżka:**

* względem minimalnej (6): +8
* względem over-provisioningu (10): +4

# Niewykorzystane adresy (wersja 1)

* 192.168.101.48/28 → 16 adresów
* 192.168.101.64/26 → 64 adresy
* 192.168.101.128/25 → 128 adresów

**Razem niewykorzystane: 208 adresów IP**
