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
  'http://localhost:8003/predict',
  'http://10.0.2.2:8003/predict',
  'http://127.0.0.1:8003/predict'
];

const CHANNELS = ['Inbound', 'Outcall', 'Email'];
const CATEGORIES = ['Returns', 'Order status', 'Product Queries', 'Cancellation', 'Feedback'];
const TENURES = ['On Job Training', '0-30', '31-60', '61-90', '>90'];
const SHIFTS = ['Morning', 'Afternoon', 'Evening', 'Night', 'Split'];

export default function App() {
  const [channel, setChannel] = useState('Inbound');
  const [category, setCategory] = useState('Returns');
  const [tenure, setTenure] = useState('>90');
  const [shift, setShift] = useState('Morning');
  const [responseTime, setResponseTime] = useState('8.5');
  const [remarks, setRemarks] = useState('Great service, the agent helped me process my refund in minutes!');

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [errorMsg, setErrorMsg] = useState('');

  const handlePredict = async () => {
    if (!responseTime) {
      Alert.alert('Thiếu thông tin', 'Vui lòng nhập thời gian phản hồi.');
      return;
    }

    setLoading(true);
    setErrorMsg('');
    setResult(null);

    const payload = {
      channel,
      category,
      tenure,
      shift,
      response_time: parseFloat(responseTime),
      remarks: remarks.trim(),
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
      setErrorMsg('Không thể kết nối đến REST API server (Port 8003). Vui lòng khởi chạy API trước.');
    }
    setLoading(false);
  };

  const isSatisfied = result && result.prediction === 1;

  return (
    <SafeAreaView style={styles.safeArea}>
      <StatusBar barStyle="light-content" backgroundColor="#4338ca" />
      <View style={styles.topBar}>
        <Text style={styles.brandTitle}>CSAT CARE MOBILE</Text>
        <Text style={styles.brandSub}>Dự đoán Hài lòng &amp; Giữ chân Khách hàng</Text>
      </View>

      <ScrollView style={styles.container} contentContainerStyle={styles.content}>
        {/* Operational */}
        <View style={styles.card}>
          <Text style={styles.cardTitle}>1. Thông số Vận hành &amp; Nhân sự</Text>

          <Text style={styles.label}>Kênh tiếp nhận (Channel)</Text>
          <View style={styles.btnGroup}>
            {CHANNELS.map((ch) => (
              <TouchableOpacity
                key={ch}
                style={[styles.choiceBtn, channel === ch && styles.choiceBtnActive]}
                onPress={() => setChannel(ch)}
              >
                <Text style={[styles.choiceText, channel === ch && styles.choiceTextActive]}>
                  {ch}
                </Text>
              </TouchableOpacity>
            ))}
          </View>

          <Text style={styles.label}>Danh mục hỗ trợ (Category)</Text>
          <View style={styles.btnGroupWrap}>
            {CATEGORIES.map((cat) => (
              <TouchableOpacity
                key={cat}
                style={[styles.choiceBtnSmall, category === cat && styles.choiceBtnActive]}
                onPress={() => setCategory(cat)}
              >
                <Text style={[styles.choiceTextSmall, category === cat && styles.choiceTextActive]}>
                  {cat}
                </Text>
              </TouchableOpacity>
            ))}
          </View>

          <Text style={styles.label}>Thời gian phản hồi (phút)</Text>
          <TextInput
            style={styles.input}
            keyboardType="numeric"
            value={responseTime}
            onChangeText={setResponseTime}
            placeholder="VD: 8.5"
          />
        </View>

        {/* NLP Multimodal */}
        <View style={styles.card}>
          <Text style={styles.cardTitle}>2. Ý kiến phản hồi của Khách (NLP)</Text>
          <TextInput
            style={[styles.input, styles.textArea]}
            multiline
            numberOfLines={3}
            value={remarks}
            onChangeText={setRemarks}
            placeholder="Nhập nội dung phản hồi, đánh giá..."
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
            <Text style={styles.submitBtnText}>DỰ ĐOÁN MỨC ĐỘ CSAT</Text>
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
          <View style={[styles.resultCard, isSatisfied ? styles.safeCard : styles.dangerCard]}>
            <Text style={styles.resultTitle}>
              {isSatisfied ? '😊 SATISFIED (HÀI LÒNG)' : '⚠️ AT-RISK (BẤT MÃN)'}
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
  safeArea: { flex: 1, backgroundColor: '#4338ca' },
  topBar: { backgroundColor: '#4338ca', padding: 16, alignItems: 'center' },
  brandTitle: { color: '#ffffff', fontSize: 18, fontWeight: '800', letterSpacing: 1 },
  brandSub: { color: '#e0e7ff', fontSize: 12, marginTop: 2 },
  container: { flex: 1, backgroundColor: '#f5f3ff' },
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
  textArea: { minHeight: 80, textAlignVertical: 'top' },
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
  choiceBtnActive: { backgroundColor: '#6366f1', borderColor: '#6366f1' },
  choiceText: { fontSize: 13, color: '#475569', fontWeight: '500' },
  choiceTextSmall: { fontSize: 12, color: '#475569', fontWeight: '500' },
  choiceTextActive: { color: '#ffffff', fontWeight: '700' },
  submitBtn: {
    backgroundColor: '#6366f1',
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
  safeCard: { backgroundColor: '#ede9fe', borderWidth: 1, borderColor: '#c4b5fd' },
  resultTitle: { fontSize: 17, fontWeight: '800', color: '#0f172a' },
  resultConfidence: { fontSize: 14, color: '#334155', marginTop: 4, fontWeight: '600' },
  resultModel: { fontSize: 12, color: '#64748b', marginTop: 4 },
});
