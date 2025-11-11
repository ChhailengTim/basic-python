# Facebook API Configuration
CONFIG = {
    'access_token': 'EAABsbCS1iHgBPAsbBd2AmKtflrbNlKZBK7COrsFYH9yNYhWwhCZCTUZA82e2WF94okViN2O5OZChA7Uv5B1itkRG6X45xWRMIOLZC6vhF6bZAjNau4lhQzsxPRuHirJoOZAa0ZBO9ZCA4ZBZA5INcF1vSMUMjVnGEWqYWUmnMvbxA8j7lRw7IJ9zIQsJ4d2PZA60Qh38vBySjnzFZCPx3H89jEwZDZD',
    'cookies': 'datr=uSJ_aKAO7bNWvTnuQl5bQZls; sb=uSJ_aNc_NF7176--xtjFfJb1; ps_l=1; ps_n=1; c_user=100009455602740; dpr=1; xs=49%3A0RwgRUOWGOm26A%3A2%3A1753162493%3A-1%3A-1%3Azkvm7KtV3AsYBw%3AAcWRKKbTX64jprWbN4h4PlQT5p6L9PA-hExcnTnHjg4M; fr=1w1vJDcDUBD0tdpur.AWcJ9vRS-dHgU5KufHPMcqGHixZtU-_5itq3v7Hnn_QsvTHE414.BoksGm..AAA.0.0.BokszW.AWefFQj-RIfdsBfqCl9Lg1_qYk4; presence=C%7B%22t3%22%3A%5B%7B%22o%22%3A0%2C%22i%22%3A%22sc.7324522240933206%22%7D%5D%2C%22utc3%22%3A1754451161242%2C%22v%22%3A1%7D; alsfid={"id":"f4dd30019","timestamp":1754451170402.7}; wd=1173x965',  # Format: "cookie1=value1; cookie2=value2"
    'page_id': '105958741845546',      # The Facebook page you want to scrape
    'output_dir': 'fb_originals',          # Organized by year/month
    'graph_api_version': 'v23.0',
    'photo_limit': 100,                    # Max 100 per request
    'max_photos': 5000,                    # Safety limit
    'retry_failed': True                   # Auto-retry failed downloads
}