import requests
import pandas as pd
from datetime import date
import time

BASE_URL = "https://parallelum.com.br/fipe/api/v1/carros"

def get_brands():
    r = requests.get(f"{BASE_URL}/marcas", timeout=20)
    r.raise_for_status()
    return r.json()

def get_models(brand_code):
    r = requests.get(f"{BASE_URL}/marcas/{brand_code}/modelos", timeout=20)
    r.raise_for_status()
    return r.json()["modelos"]

def get_years(brand_code, model_code):
    r = requests.get(f"{BASE_URL}/marcas/{brand_code}/modelos/{model_code}/anos", timeout=20)
    r.raise_for_status()
    return r.json()

def get_price(brand_code, model_code, year_code):
    r = requests.get(
        f"{BASE_URL}/marcas/{brand_code}/modelos/{model_code}/anos/{year_code}",
        timeout=20
    )
    r.raise_for_status()
    return r.json()

def main():
    brands = get_brands()
    data = []

    for brand in brands[:5]:  # 先取前5个品牌
        brand_name = brand["nome"]
        brand_code = brand["codigo"]
        print(f"正在抓取品牌: {brand_name}")

        try:
            models = get_models(brand_code)

            for model in models[:5]:  # 每个品牌取前5个车型
                model_name = model["nome"]
                model_code = model["codigo"]

                years = get_years(brand_code, model_code)

                for year in years[:3]:  # 每个车型取前3个年份
                    year_code = year["codigo"]

                    try:
                        detail = get_price(brand_code, model_code, year_code)

                        data.append({
                            "brand": detail.get("Marca"),
                            "model": detail.get("Modelo"),
                            "year": detail.get("AnoModelo"),
                            "fuel": detail.get("Combustivel"),
                            "price": detail.get("Valor"),
                            "currency": "BRL",
                            "reference_month": detail.get("MesReferencia"),
                            "fipe_code": detail.get("CodigoFipe"),
                            "source": "FIPE API",
                            "date": date.today()
                        })

                        time.sleep(0.3)

                    except Exception as e:
                        print(f"价格抓取失败: {brand_name} {model_name} {year_code} - {e}")

        except Exception as e:
            print(f"{brand_name} 抓取失败：{e}")

    df = pd.DataFrame(data)
    df.to_csv("brazil_car_full_price_data.csv", index=False, encoding="utf-8-sig")

    print(df)
    print("已保存 brazil_car_full_price_data.csv")

if __name__ == "__main__":
    main()
    