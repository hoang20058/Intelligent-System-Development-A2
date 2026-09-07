import React, { useState } from 'react';
import {
  StyleSheet,
  Text,
  View,
  ScrollView,
  TextInput,
  TouchableOpacity,
  ActivityIndicator,
  Alert,
  SafeAreaView,
  StatusBar
} from 'react-native';

const API_ENDPOINTS = [
  'http://localhost:8002/predict',
  'http://10.0.2.2:8002/predict',
  'http://127.0.0.1:8002/predict'
];

const POPULAR_STATES = ['California', 'New York', 'Texas', 'Florida', 'Massachusetts', 'New Jersey', 'Washington'];

export default function App() {
  const [bed, setBed] = useState('3');
  const [bath, setBath] = useState('2');
  const [houseSize, setHouseSize] = useState('1850');
  const [acreLot, setAcreLot] = useState('0.25');
  const [state, setState] = useState('California');
  const [city, setCity] = useState('Los Angeles');
  const [status, setStatus] = useState('for_sale');

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [errorMsg, setErrorMsg] = useState('');

  const handlePredict = async () => {
    if (!bed || !bath || !houseSize || !acreLot) {
      Alert.alert('Thiếu thông tin', 'Vui lòng nhập đầy đủ các thông số nhà ở.');
      return;
    }

    setLoading(true);
    setErrorMsg('');
    setResult(null);

    const payload = {
      bed: parseInt(bed, 10),
      bath: parseInt(bath, 10),
      house_size: parseFloat(houseSize),
      acre_lot: parseFloat(acreLot),
      state,
      city,
      status,
    };

    let success = false;
    for (const url of API_ENDPOINTS) {
      try {
        const response = await fetch(url, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        });

        if (response.ok) {
          const data = await response.json();
          setResult(data);
          success = true;
          break;
        }
      } catch (err) {}
    }

    if (!success) {
      setErrorMsg('Không thể kết nối đến REST API server (Port 8002). Vui lòng khởi chạy API trước.');
    }
    setLoading(false);
  };

  return (
    <SafeAreaView style={styles.safeArea}>
      <StatusBar barStyle="light-content" backgroundColor="#1e40af" />
      <View style={styles.topBar}>
        <Text style={styles.brandTitle}>REALESTATE MOBILE</Text>
        <Text style={styles.brandSub}>Định giá Bất động sản Hoa Kỳ</Text>
      </View>

      <ScrollView style={styles.container} contentContainerStyle={styles.content}>
        {/* Physical Features */}
        <View style={styles.card}>
          <Text style={styles.cardTitle}>1. Thông số Căn hộ / Nhà ở</Text>

          <View style={styles.row}>
            <View style={styles.col}>
              <Text style={styles.label}>Phòng ngủ (Bed)</Text>
              <TextInput
                style={styles.input}
                keyboardType="numeric"
                value={bed}
                onChangeText={setBed}
                placeholder="VD: 3"
              />
            </View>
            <View style={styles.col}>
              <Text style={styles.label}>Phòng tắm (Bath)</Text>
              <TextInput
                style={styles.input}
                keyboardType="numeric"
                value={bath}
                onChangeText={setBath}
                placeholder="VD: 2"
              />
            </View>
          </View>

          <Text style={styles.label}>Diện tích sàn (sqft)</Text>
          <TextInput
            style={styles.input}
            keyboardType="numeric"
            value={houseSize}
            onChangeText={setHouseSize}
            placeholder="VD: 1850 (1 sqft ≈ 0.093 m²)"
          />

          <Text style={styles.label}>Diện tích khuôn viên (Acre)</Text>
          <TextInput
            style={styles.input}
            keyboardType="numeric"
            value={acreLot}
            onChangeText={setAcreLot}
            placeholder="VD: 0.25 (1 acre ≈ 4047 m²)"
          />
        </View>

        {/* Location & Status */}
        <View style={styles.card}>
          <Text style={styles.cardTitle}>2. Vị trí &amp; Tình trạng</Text>

          <Text style={styles.label}>Tiểu bang (State)</Text>
          <View style={styles.btnGroupWrap}>
            {POPULAR_STATES.map((s) => (
              <TouchableOpacity
                key={s}
                style={[styles.stateBtn, state === s && styles.stateBtnActive]}
                onPress={() => setState(s)}
              >
                <Text style={[styles.stateBtnText, state === s && styles.stateBtnTextActive]}>
                  {s}
                </Text>
              </TouchableOpacity>
            ))}
          </View>

          <Text style={styles.label}>Thành phố (City)</Text>
          <TextInput
            style={styles.input}
            value={city}
            onChangeText={setCity}
            placeholder="VD: Los Angeles, Houston..."
          />
        </View>

        {/* Submit Button */}
        <TouchableOpacity
          style={styles.submitBtn}
          onPress={handlePredict}
          disabled={loading}
        >
          {loading ? (
            <ActivityIndicator color="#fff" />
          ) : (
            <Text style={styles.submitBtnText}>ƯỚC TÍNH GIÁ TRỊ NHÀ Ở (USD)</Text>
          )}
        </TouchableOpacity>

        {/* Error */}
        {errorMsg !== '' && (
          <View style={styles.errorBox}>
            <Text style={styles.errorText}>⚠️ {errorMsg}</Text>
          </View>
        )}

        {/* Result */}
        {result && (
          <View style={styles.resultCard}>
            <Text style={styles.resultPriceLabel}>GIÁ TRỊ ƯỚC TÍNH THỊ TRƯỜNG</Text>
            <Text style={styles.resultPrice}>{result.formatted}</Text>
            <Text style={styles.resultModel}>Mô hình: {result.model_used}</Text>
          </View>
        )}
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: { flex: 1, backgroundColor: '#1e40af' },
  topBar: { backgroundColor: '#1e40af', padding: 16, alignItems: 'center' },
  brandTitle: { color: '#ffffff', fontSize: 18, fontWeight: '800', letterSpacing: 1 },
  brandSub: { color: '#bfdbfe', fontSize: 12, marginTop: 2 },
  container: { flex: 1, backgroundColor: '#f0f9ff' },
  content: { padding: 16, paddingBottom: 40 },
  card: {
    backgroundColor: '#ffffff',
    borderRadius: 16,
    padding: 16,
    marginBottom: 16,
    borderWidth: 1,
    borderColor: '#e2e8f0',
  },
  cardTitle: { fontSize: 15, fontWeight: '700', color: '#0f172a', marginBottom: 12 },
  row: { flexDirection: 'row', gap: 10 },
  col: { flex: 1 },
  label: { fontSize: 13, fontWeight: '600', color: '#334155', marginTop: 10, marginBottom: 6 },
  input: {
    borderWidth: 1,
    borderColor: '#cbd5e1',
    borderRadius: 10,
    paddingHorizontal: 12,
    paddingVertical: 10,
    fontSize: 14,
    backgroundColor: '#f8fafc',
    color: '#0f172a',
  },
  btnGroupWrap: { flexDirection: 'row', flexWrap: 'wrap', gap: 6 },
  stateBtn: {
    paddingHorizontal: 10,
    paddingVertical: 6,
    borderRadius: 8,
    backgroundColor: '#f1f5f9',
    borderWidth: 1,
    borderColor: '#e2e8f0',
  },
  stateBtnActive: { backgroundColor: '#2563eb', borderColor: '#2563eb' },
  stateBtnText: { fontSize: 12, color: '#475569', fontWeight: '500' },
  stateBtnTextActive: { color: '#ffffff', fontWeight: '700' },
  submitBtn: {
    backgroundColor: '#2563eb',
    paddingVertical: 16,
    borderRadius: 14,
    alignItems: 'center',
    marginVertical: 10,
  },
  submitBtnText: { color: '#ffffff', fontSize: 14, fontWeight: '700' },
  errorBox: { backgroundColor: '#fef2f2', padding: 12, borderRadius: 10, marginVertical: 8 },
  errorText: { color: '#b91c1c', fontSize: 13, textAlign: 'center' },
  resultCard: {
    backgroundColor: '#eff6ff',
    borderWidth: 2,
    borderColor: '#93c5fd',
    padding: 20,
    borderRadius: 16,
    marginTop: 12,
    alignItems: 'center',
  },
  resultPriceLabel: { fontSize: 12, fontWeight: '700', color: '#1d4ed8', letterSpacing: 0.5 },
  resultPrice: { fontSize: 32, fontWeight: '900', color: '#1e3a8a', marginVertical: 6 },
  resultModel: { fontSize: 12, color: '#64748b' },
});
