import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'pennywise.db')

conn = sqlite3.connect(DB_PATH)


updates = [
    
    ('https://images.unsplash.com/photo-1616592079624-575de673daff?q=80&w=387&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D', 1), 
    ('https://images.unsplash.com/photo-1773372238324-e9cffa5f45b7?q=80&w=396&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D', 2),  
    ('https://images.unsplash.com/photo-1557205465-f3762edea6d3?q=80&w=387&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D', 3),  
    ('https://images.unsplash.com/photo-1631214540553-ff044a3ff1d4?q=80&w=774&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D', 4), 
    ('https://images.unsplash.com/photo-1768983224486-b4dcd179b4a5?q=80&w=387&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D', 5),  
    ('https://images.unsplash.com/photo-1631214499500-2e34edcaccfe?q=80&w=415&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D', 6),  
    ('https://images.unsplash.com/photo-1547887538-e3a2f32cb1cc?q=80&w=870&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D', 7),  
    ('https://images.unsplash.com/photo-1704621354783-15f5741ff4de?q=80&w=1374&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D', 8), 
    ('https://images.unsplash.com/photo-1515688594390-b649af70d282?q=80&w=806&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D', 9),  
    ('https://images.unsplash.com/photo-1752245818739-890854ca3b81?q=80&w=387&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D', 10),  
    ('https://images.unsplash.com/photo-1583334529937-bc4761d2cdad?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8N3x8bW9pc3RlcmlzZXJ8ZW58MHx8MHx8fDA%3D', 11),  
    ('https://images.unsplash.com/photo-1556228720-195a672e8a03?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8Y2xlYW5zZXJ8ZW58MHx8MHx8fDA%3D', 12),  
    ('https://images.unsplash.com/photo-1679394270597-e90694d70350?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8c2VydW18ZW58MHx8MHx8fDA%3D', 13),  
    ('https://images.unsplash.com/photo-1616986953793-2e6159b78580?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8dG9uZXJ8ZW58MHx8MHx8fDA%3D', 14),  # Shampoo
    ('https://images.unsplash.com/photo-1582020738577-2e7a48043902?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTh8fG5pZ2h0JTIwY3JlYW18ZW58MHx8MHx8fDA%3D', 15),  # Perfume
    ('https://images.unsplash.com/photo-1594332322527-08753d4473c1?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8c3Vuc2NyZWVuJTIwbG90aW9ufGVufDB8fDB8fHww', 16),  # Eyeliner
    ('https://images.unsplash.com/photo-1606874576257-5400d9711ce1?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8ZmFjZSUyMHNjcnVifGVufDB8fDB8fHww', 17),  # Lipstick
    ('https://images.unsplash.com/photo-1743926959711-73960c2a7b4e?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8aHlhbHVyb25pYyUyMGFjaWQlMjBtaXN0fGVufDB8fDB8fHww', 18),  # Moisturizer
    ('https://images.unsplash.com/photo-1700709678003-01941f72fb92?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTF8fHNoYW1wb298ZW58MHx8MHx8fDA%3D', 19),  # Shampoo
    ('https://images.unsplash.com/photo-1730115656817-92eb256f2c01?q=80&w=870&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D', 20),  # Perfume
    ('https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8N3x8aGFpciUyMG1hc2t8ZW58MHx8MHx8fDA%3D', 21),  # Eyeliner
    ('https://images.unsplash.com/photo-1701977501667-20c0e38f5a9d?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8OHx8aGFpciUyMHByb3RlY3Rpb24lMjBzcHJheXxlbnwwfHwwfHx8MA%3D%3D', 22),  # Lipstick
    ('https://images.unsplash.com/photo-1515377905703-c4788e51af15?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8aGFpciUyMG9pbHxlbnwwfHwwfHx8MA%3D%3D', 23),  # Moisturizer
    ('https://images.unsplash.com/photo-1770801153497-959241fce3ae?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8aGFpcmNhcmUlMjBraXR8ZW58MHx8MHx8fDA%3D', 24),  # Shampoo
    ('https://images.unsplash.com/photo-1541643600914-78b084683601?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8cGVyZnVtZXxlbnwwfHwwfHx8MA%3D%3D', 25),  # Perfume
    ('https://images.unsplash.com/photo-1623085080484-623ff2873922?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8Y2l0cnVzJTIwcGVyZnVtZXxlbnwwfHwwfHx8MA%3D%3D', 26),  # Eyeliner
    ('https://images.unsplash.com/photo-1693734464091-09942cdb6ca0?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8ZWF1JTIwZGUlMjBwYXJmdW18ZW58MHx8MHx8fDA%3D', 27),  # Lipstick
    ('https://images.unsplash.com/photo-1671642605304-2a0a812b5529?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8Ym9keSUyMG1pc3R8ZW58MHx8MHx8fDA%3D', 28),  # Moisturizer
    ('https://images.unsplash.com/photo-1636833777376-4487142e8e17?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8cGVyZnVtZSUyMHNldHxlbnwwfHwwfHx8MA%3D%3D', 29),  # Shampoo
    ('https://images.unsplash.com/photo-1703174323653-0455deaf7f11?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8c2hlYSUyMGJ1dHRlciUyMGJvZHklMjBsb3Rpb258ZW58MHx8MHx8fDA%3D', 30),  # Perfume
    ('https://images.unsplash.com/photo-1669212408959-fdde3b2ed6a2?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8Ym9keSUyMHdhc2h8ZW58MHx8MHx8fDA%3D', 31),  # Eyeliner
    ('https://images.unsplash.com/photo-1683944433023-027a3f443ae4?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8Ym9keSUyMHNjcnVifGVufDB8fDB8fHww', 32),  # Lipstick
    ('https://images.unsplash.com/photo-1621483942660-48b49739ac3b?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8YmF0aCUyMGJvbWIlMjBzZXR8ZW58MHx8MHx8fDA%3D', 33),  # Moisturizer
    ('https://images.unsplash.com/photo-1601065732058-029db52c86b4?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8aGFuZCUyMGNyZWFtfGVufDB8fDB8fHww', 34),  # Shampoo
    ('https://images.unsplash.com/photo-1627495395570-d2c94e3319f5?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8bGlxdWlkJTIwc29hcHxlbnwwfHwwfHx8MA%3D%3D', 35),  # Perfume
    ('https://images.unsplash.com/photo-1637524725461-bff1afdb946e?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8N3x8Ym9keSUyMG9pbHxlbnwwfHwwfHx8MA%3D%3D', 36),  # Eyeliner

]

for url, pid in updates:
    conn.execute('UPDATE products SET image_url=? WHERE id=?', (url, pid))
    print(f'Updated product {pid}')

conn.commit()
conn.close()
print('Done!')