import { StatusBar } from 'expo-status-bar';
import { useState, useRef } from 'react';
import { StyleSheet, Text, View, TextInput, TouchableOpacity, ScrollView, SafeAreaView, KeyboardAvoidingView, Platform } from 'react-native';

export default function App() {
    const [messages, setMessages] = useState([
        { role: 'assistant', content: 'Hello! I am MetaChat AI. How can I help you?' }
    ]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const scrollViewRef = useRef();

    const handleSend = async () => {
        if (!input.trim()) return;

        const userMsg = input;
        setMessages(prev => [...prev, { role: 'user', content: userMsg }]);
        setInput('');
        setIsLoading(true);

        try {
            // 10.0.2.2 is localhost for Android Emulator
            const response = await fetch('http://10.0.2.2:8000/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: userMsg }),
            });

            const text = await response.text();
            setMessages(prev => [...prev, { role: 'assistant', content: text }]);
        } catch (error) {
            setMessages(prev => [...prev, { role: 'assistant', content: 'Error connecting to server. Make sure Backend is running.' }]);
            console.error(error);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <SafeAreaView style={styles.container}>
            <StatusBar style="auto" />
            <View style={styles.header}>
                <Text style={styles.headerTitle}>MetaChat AI</Text>
            </View>

            <ScrollView
                style={styles.chatArea}
                ref={scrollViewRef}
                onContentSizeChange={() => scrollViewRef.current.scrollToEnd({ animated: true })}
            >
                {messages.map((msg, index) => (
                    <View key={index} style={[
                        styles.messageBubble,
                        msg.role === 'user' ? styles.userBubble : styles.aiBubble
                    ]}>
                        <Text style={[
                            styles.messageText,
                            msg.role === 'user' ? styles.userText : styles.aiText
                        ]}>{msg.content}</Text>
                    </View>
                ))}
                {isLoading && <Text style={styles.loadingText}>Thinking...</Text>}
            </ScrollView>

            <KeyboardAvoidingView behavior={Platform.OS === 'ios' ? 'padding' : 'height'} style={styles.inputArea}>
                <TextInput
                    style={styles.input}
                    value={input}
                    onChangeText={setInput}
                    placeholder="Type a message..."
                />
                <TouchableOpacity onPress={handleSend} style={styles.sendButton}>
                    <Text style={styles.sendButtonText}>Send</Text>
                </TouchableOpacity>
            </KeyboardAvoidingView>
        </SafeAreaView>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#fff',
    },
    header: {
        padding: 20,
        backgroundColor: '#f8f9fa',
        borderBottomWidth: 1,
        borderBottomColor: '#eee',
        marginTop: 30,
    },
    headerTitle: {
        fontSize: 20,
        fontWeight: 'bold',
        color: '#0064e0',
    },
    chatArea: {
        flex: 1,
        padding: 15,
    },
    messageBubble: {
        padding: 15,
        borderRadius: 20,
        marginBottom: 10,
        maxWidth: '80%',
    },
    userBubble: {
        backgroundColor: '#0064e0',
        alignSelf: 'flex-end',
        borderBottomRightRadius: 2,
    },
    aiBubble: {
        backgroundColor: '#f0f2f5',
        alignSelf: 'flex-start',
        borderBottomLeftRadius: 2,
    },
    messageText: {
        fontSize: 16,
    },
    userText: {
        color: '#fff',
    },
    aiText: {
        color: '#000',
    },
    loadingText: {
        marginLeft: 10,
        marginTop: 5,
        marginBottom: 10,
        color: '#888',
        fontStyle: 'italic',
    },
    inputArea: {
        flexDirection: 'row',
        padding: 15,
        borderTopWidth: 1,
        borderTopColor: '#eee',
        alignItems: 'center',
    },
    input: {
        flex: 1,
        backgroundColor: '#f0f2f5',
        borderRadius: 25,
        paddingHorizontal: 20,
        paddingVertical: 10,
        marginRight: 10,
        fontSize: 16,
    },
    sendButton: {
        backgroundColor: '#0064e0',
        paddingVertical: 10,
        paddingHorizontal: 20,
        borderRadius: 25,
    },
    sendButtonText: {
        color: '#fff',
        fontWeight: 'bold',
    },
});
