import tkinter as tk
from tkinter import ttk
from sklearn.tree import DecisionTreeClassifier
from sklearn import preprocessing
import pandas as pd

# Hàm xây dựng mô hình ID3
def ID3():
    # Đọc dữ liệu từ file CSV
    data = pd.read_csv('weather_data.csv')

    # Xác định đặc trưng và nhãn
    dac_trung = data.drop('Weather', axis=1)
    nhan = data['Weather']

    # Chuyển đổi văn bản thành số
    nhan_encoded = preprocessing.LabelEncoder()
    dac_trung_encoded = dac_trung.apply(nhan_encoded.fit_transform)

    # Xây dựng mô hình ID3
    model = DecisionTreeClassifier()
    model.fit(dac_trung_encoded, nhan)

    return model, nhan_encoded

# Hàm để dự đoán thời tiết
def du_bao(model, nhan_encoded, temperature, humidity, wind):
    # Tạo DataFrame mới từ dữ liệu nhập vào
    new_data = pd.DataFrame({'Temperature': [temperature], 'Humidity': [humidity], 'Wind': [wind]})
    # Dự đoán thời tiết
    predicted_weather = model.predict(new_data)
    return predicted_weather[0]

# Hàm xử lý khi nhấn nút dự đoán
def du_bao_thoi_tiet():
    temperature = temperature_entry.get()
    humidity = humidity_entry.get()
    wind_str = wind_combobox.get().title()  # Chuẩn hoá giá trị nhập vào

    # Gán giá trị của cột "Wind" theo yêu cầu
    if wind_str == 'Mạnh':
        wind_encoded = 0
    elif wind_str == 'Trung Bình':
        wind_encoded = 1
    elif wind_str == 'Nhẹ':
        wind_encoded = 2

    # Dự đoán thời tiết
    result = du_bao(model, nhan_encoded, temperature, humidity, wind_encoded)

    # Hiển thị kết quả
    result_label.config(text=f'Kết quả: {result}')


def reset():
    temperature_entry.delete(0, tk.END)
    humidity_entry.delete(0, tk.END)
    wind_combobox.set('')  
    result_label.config(text='Kết quả: ')

# Tạo cửa sổ ứng dụng
app = tk.Tk()
app.title('Dự báo Thời tiết')
app.geometry('500x270')

# Xây dựng mô hình khi khởi động ứng dụng
model, nhan_encoded = ID3()

# Tạo và định cấu hình giao diện người dùng
frame = ttk.Frame(app, padding='10')
frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

temperature_label = ttk.Label(frame, text='Nhiệt độ (°C):', font=('Calibri', 16, ''))
temperature_label.grid(column=0, row=0, sticky=tk.E, padx=5, pady=5)
temperature_entry = ttk.Entry(frame, font=('Calibri', 16, ''))
temperature_entry.grid(column=1, row=0, sticky=tk.W)

humidity_label = ttk.Label(frame, text='Độ ẩm (%):', font=('Calibri', 16, ''))
humidity_label.grid(column=0, row=1, sticky=tk.E, padx=5, pady=5)
humidity_entry = ttk.Entry(frame, font=('Calibri', 16, ''))
humidity_entry.grid(column=1, row=1, sticky=tk.W)

wind_label = ttk.Label(frame, text='Tốc độ gió:', font=('Calibri', 16, ''))
wind_label.grid(column=0, row=2, sticky=tk.E, padx=5, pady=5)
wind_combobox = ttk.Combobox(frame, values=['Mạnh', 'Trung Bình', 'Nhẹ'], font=('Calibri', 16, ''), width=18)
wind_combobox.grid(column=1, row=2, sticky=tk.W)

style = ttk.Style()
style.configure('TButton', font=('Calibri', 16, ''))

predict_button = ttk.Button(frame, text='Dự đoán', command=du_bao_thoi_tiet, style='TButton', width=8)
predict_button.grid(column=1, row=3, sticky=tk.W, padx=0, pady=10)

reset_button = ttk.Button(frame, text='Reset', command=reset, style='TButton', width=8)
reset_button.grid(column=1, row=3, sticky=tk.W, padx=125, pady=10)

result_label = ttk.Label(frame, text='Kết quả: ', font=('Calibri', 16, ''))
result_label.grid(column=0, row=4, columnspan=2, sticky=tk.W, padx=90, pady=10)

app.mainloop()
