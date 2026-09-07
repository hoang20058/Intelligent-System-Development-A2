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
  StatusBar,
  Platform
} from 'react-native';

const API_ENDPOINTS = [
  'http://localhost:8001/predict',
  'http://10.0.2.2:8001/predict',
  'http://127.0.0.1:8001/predict'
];

export default function App() {
  const [gender, setGender] = useState('Female');
  const [age, setAge] = useState('45');
  const [race, setRace] = useState('Caucasian');
  const [hypertension, setHypertension] = useState(0);
  const [heartDisease, setHeartDisease] = useState(0);
  const [smoking, setSmoking] = useState('never');
  const [bmi, setBmi] = useState('27.5');
  const [hba1c, setHba1c] = useState('6.2');
  const [glucose, setGlucose] = useState('135');

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [errorMsg, setErrorMsg] = useState('');

  const handlePredict = async () => {
    if (!age || !bmi || !hba1c || !glucose) {
      Alert.alert('Thiếu thông tin', 'Vui lòng nhập đầy đủ các chỉ số sinh hóa.');
      return;
    }

    setLoading(true);
    setErrorMsg('');
    setResult(null);

    const payload = {
      gender,
      age: parseInt(age, 10),
      race,
      hypertension: parseInt(hypertension, 10),
      heart_disease: parseInt(heartDisease, 10),
      smoking_history: smoking,
      bmi: parseFloat(bmi),
      hbA1c_level: parseFloat(hba1c),
      blood_glucose_level: parseInt(glucose, 10),
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
      } catch (err) {
        // continue trying next endpoint
      }
    }

    if (!success) {
      setErrorMsg('Không thể kết nối đến REST API server (Port 8001). Vui lòng khởi chạy API trước.');
    }
    setLoading(false);
  };

  const isDiabetic = result && result.prediction === 1;

  return (
    <SafeAreaView style={styles.safeArea}>
      <StatusBar barStyle="light-content" backgroundColor="#047857" />
      <View style={styles.topBar}>
        <Text style={styles.brandTitle}>HEALTHSCREEN MOBILE</Text>
        <Text style={styles.brandSub}>Chẩn đoán Sàng lọc Nguy cơ Tiểu đường</Text>
      </View>

      <ScrollView style={styles.container} contentContainerStyle={styles.content}>
        {/* Basic Info */}
        <View style={styles.card}>
          <Text style={styles.cardTitle}>1. Thông tin Bệnh nhân</Text>

          <Text style={styles.label}>Giới tính</Text>
          <View style={styles.btnGroup}>
            {['Female', 'Male', 'Other'].map((item) => (
              <TouchableOpacity
                key={item}
                style={[styles.choiceBtn, gender === item && styles.choiceBtnActive]}
                onPress={() => setGender(item)}
              >
                <Text style={[styles.choiceText, gender === item && styles.choiceTextActive]}>
                  {item === 'Female' ? 'Nữ' : item === 'Male' ? 'Nam' : 'Khác'}
                </Text>
              </TouchableOpacity>
            ))}
          </View>

          <Text style={styles.label}>Tuổi</Text>
          <TextInput
            style={styles.input}
            keyboardType="numeric"
            value={age}
            onChangeText={setAge}
            placeholder="VD: 45"
          />

          <Text style={styles.label}>Chủng tộc</Text>
          <View style={styles.btnGroupWrap}>
            {['Caucasian', 'Asian', 'AfricanAmerican', 'Hispanic', 'Other'].map((item) => (
              <TouchableOpacity
                key={item}
                style={[styles.choiceBtnSmall, race === item && styles.choiceBtnActive]}
                onPress={() => setRace(item)}
              >
                <Text style={[styles.choiceTextSmall, race === item && styles.choiceTextActive]}>
                  {item}
                </Text>
              </TouchableOpacity>
            ))}
          </View>
        </View>

        {/* Clinical Parameters */}
        <View style={styles.card}>
          <Text style={styles.cardTitle}>2. Chỉ số Sinh hóa</Text>

          <Text style={styles.label}>Chỉ số BMI (kg/m²)</Text>
          <TextInput
            style={styles.input}
            keyboardType="numeric"
            value={bmi}
            onChangeText={setBmi}
            placeholder="VD: 27.5"
          />

          <Text style={styles.label}>Chỉ số HbA1c (%)</Text>
          <TextInput
            style={styles.input}
            keyboardType="numeric"
            value={hba1c}
            onChangeText={setHba1c}
            placeholder="VD: 6.2 (Bình thường: <5.7)"
          />

          <Text style={styles.label}>Đường huyết ngẫu nhiên (mg/dL)</Text>
          <TextInput
            style={styles.input}
            keyboardType="numeric"
            value={glucose}
            onChangeText={setGlucose}
            placeholder="VD: 135 (Bình thường: <140)"
          />
        </View>

        {/* Submit */}
        <TouchableOpacity
          style={styles.submitBtn}
          onPress={handlePredict}
          disabled={loading}
        >
          {loading ? (
            <ActivityIndicator color="#fff" />
          ) : (
            <Text style={styles.submitBtnText}>CHẨN ĐOÁN NGUY CƠ TIỂU ĐƯỜNG</Text>
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
          <View style={[styles.resultCard, isDiabetic ? styles.dangerCard : styles.safeCard]}>
            <Text style={styles.resultTitle}>
              {isDiabetic ? '🚨 CÓ NGUY CƠ TIỂU ĐƯỜNG' : '✅ KHÔNG CÓ NGUY CƠ'}
            </Text>
            <Text style={styles.resultConfidence}>
              Độ tin cậy: {result.confidence}%
            </Text>
            <Text style={styles.resultModel}>Mô hình: {result.model_used}</Text>
          </View>
        )}
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: { flex: 1, backgroundColor: '#047857' },
  topBar: { backgroundColor: '#047857', padding: 16, alignItems: 'center' },
  brandTitle: { color: '#ffffff', fontSize: 18, fontWeight: '800', letterSpacing: 1 },
  brandSub: { color: '#d1fae5', fontSize: 12, marginTop: 2 },
  container: { flex: 1, backgroundColor: '#f0fdf4' },
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
  btnGroup: { flexDirection: 'row', gap: 8 },
  btnGroupWrap: { flexDirection: 'row', flexWrap: 'wrap', gap: 6 },
  choiceBtn: {
    flex: 1,
    paddingVertical: 9,
    alignItems: 'center',
    borderRadius: 8,
    backgroundColor: '#f1f5f9',
    borderWidth: 1,
    borderColor: '#e2e8f0',
  },
  choiceBtnSmall: {
    paddingHorizontal: 12,
    paddingVertical: 7,
    borderRadius: 8,
    backgroundColor: '#f1f5f9',
    borderWidth: 1,
    borderColor: '#e2e8f0',
  },
  choiceBtnActive: { backgroundColor: '#059669', borderColor: '#059669' },
  choiceText: { fontSize: 13, color: '#475569', fontWeight: '500' },
  choiceTextSmall: { fontSize: 12, color: '#475569', fontWeight: '500' },
  choiceTextActive: { color: '#ffffff', fontWeight: '700' },
  submitBtn: {
    backgroundColor: '#059669',
    paddingVertical: 16,
    borderRadius: 14,
    alignItems: 'center',
    marginVertical: 10,
  },
  submitBtnText: { color: '#ffffff', fontSize: 14, fontWeight: '700' },
  errorBox: { backgroundColor: '#fef2f2', padding: 12, borderRadius: 10, marginVertical: 8 },
  errorText: { color: '#b91c1c', fontSize: 13, textAlign: 'center' },
  resultCard: { padding: 18, borderRadius: 14, marginTop: 12, alignItems: 'center' },
  dangerCard: { backgroundColor: '#fee2e2', borderWidth: 1, borderColor: '#fca5a5' },
  safeCard: { backgroundColor: '#dcfce7', borderWidth: 1, borderColor: '#86efac' },
  resultTitle: { fontSize: 17, fontWeight: '800', color: '#0f172a' },
  resultConfidence: { fontSize: 14, color: '#334155', marginTop: 4, fontWeight: '600' },
  resultModel: { fontSize: 12, color: '#64748b', marginTop: 4 },
});
