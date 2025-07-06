import React, { useState, useRef, useEffect, useCallback } from 'react';
import { Send, BookOpen, User, Award, FileText, Download, MessageCircle, Brain, GraduationCap, ClipboardCheck, Settings, LogOut, ChevronRight, Play, Pause, Volume2, Mic, MicOff } from 'lucide-react';

const AIMentorPlatform = () => {
    const [messages, setMessages] = useState([]);
    const [inputText, setInputText] = useState('');
    const [loading, setLoading] = useState(false);
    const [studentId, setStudentId] = useState(1);
    const [studentData, setStudentData] = useState(null);
    const [currentContent, setCurrentContent] = useState(null);
    const [isRecording, setIsRecording] = useState(false);
    const [connectionStatus, setConnectionStatus] = useState('connected');

    const messagesEndRef = useRef(null);
    const chatContainerRef = useRef(null);

    const API_BASE_URL = 'http://localhost:8000/api/v1';

    // Expert configurations
    const expertConfig = {
        registrator: {
            name: 'Консультант',
            icon: User,
            gradient: 'from-blue-500 to-indigo-600',
            description: 'Регистрация и настройка профиля',
            avatar: '👋'
        },
        interview: {
            name: 'Аналитик',
            icon: MessageCircle,
            gradient: 'from-purple-500 to-pink-600',
            description: 'Анализ потребностей и планирование',
            avatar: '🎯'
        },
        teacher: {
            name: 'Наставник',
            icon: GraduationCap,
            gradient: 'from-emerald-500 to-teal-600',
            description: 'Обучение и развитие навыков',
            avatar: '📚'
        },
        test: {
            name: 'Эксперт',
            icon: ClipboardCheck,
            gradient: 'from-amber-500 to-orange-600',
            description: 'Оценка знаний и сертификация',
            avatar: '⭐'
        }
    };

    // API calls
    const apiCall = useCallback(async (endpoint, options = {}) => {
        try {
            setConnectionStatus('connecting');
            const response = await fetch(`${API_BASE_URL}${endpoint}`, {
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers,
                },
                ...options,
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            setConnectionStatus('connected');
            return await response.json();
        } catch (error) {
            setConnectionStatus('error');
            console.error('API Error:', error);
            throw error;
        }
    }, [API_BASE_URL]);

    const fetchStudentData = useCallback(async () => {
        try {
            const data = await apiCall(`/edu/student/${studentId}`);
            setStudentData(data);
        } catch (error) {
            console.error('Failed to fetch student data:', error);
        }
    }, [studentId, apiCall]);

    const sendMessage = async () => {
        if (!inputText.trim() || loading) return;

        const userMessage = {
            id: Date.now(),
            role: 'user',
            text: inputText.trim(),
            timestamp: new Date().toISOString()
        };

        setMessages(prev => [...prev, userMessage]);
        setInputText('');
        setLoading(true);

        try {
            const response = await apiCall('/chat/message/send', {
                method: 'POST',
                body: JSON.stringify({
                    student_id: studentId,
                    text: inputText.trim()
                })
            });

            const assistantMessage = {
                id: Date.now() + 1,
                role: 'assistant',
                text: response.user_message,
                timestamp: new Date().toISOString(),
                commands: response.commands || []
            };

            setMessages(prev => [...prev, assistantMessage]);

            // Refresh student data if there were commands
            if (response.commands && response.commands.length > 0) {
                await fetchStudentData();
            }

        } catch (error) {
            const errorMessage = {
                id: Date.now() + 1,
                role: 'assistant',
                text: 'Извините, произошла ошибка. Попробуйте еще раз.',
                timestamp: new Date().toISOString(),
                isError: true
            };
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setLoading(false);
        }
    };

    const downloadContent = async (contentType, contentId) => {
        try {
            const response = await fetch(`${API_BASE_URL}/edu/topic/download/${contentType}/${contentId}`);
            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `content-${contentId}.pdf`;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
            }
        } catch (error) {
            console.error('Download failed:', error);
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    };

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    useEffect(() => {
        fetchStudentData();
    }, [fetchStudentData]);

    const getCurrentExpert = () => {
        return studentData?.current_expert || 'registrator';
    };

    const getProgressPercentage = () => {
        if (!studentData) return 0;

        const totalItems = 45; // Примерное общее количество элементов
        const completed =
            Object.keys(studentData.approved_topics || {}).length +
            Object.keys(studentData.approved_blocks || {}).length +
            Object.keys(studentData.approved_chapters || {}).length;

        return Math.round((completed / totalItems) * 100);
    };

    const currentExpert = getCurrentExpert();
    const expertInfo = expertConfig[currentExpert] || expertConfig.registrator;
    const progressPercentage = getProgressPercentage();

    const ConnectionIndicator = () => (
        <div className="flex items-center space-x-2">
            <div className={`w-2 h-2 rounded-full ${
                connectionStatus === 'connected' ? 'bg-emerald-400 animate-pulse' :
                    connectionStatus === 'connecting' ? 'bg-amber-400 animate-spin' :
                        'bg-red-400'
            }`}></div>
            <span className="text-sm text-gray-600">
        {connectionStatus === 'connected' ? 'Онлайн' :
            connectionStatus === 'connecting' ? 'Подключение...' :
                'Ошибка соединения'}
      </span>
        </div>
    );

    return (
        <div className="h-screen bg-gradient-to-br from-slate-50 to-blue-50 flex flex-col">
            {/* Modern Header */}
            <header className="bg-white/80 backdrop-blur-lg border-b border-gray-200/50 px-6 py-4 shadow-sm">
                <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-6">
                        <div className="flex items-center space-x-3">
                            <div className="relative">
                                <Brain className="w-10 h-10 text-indigo-600" />
                                <div className="absolute -top-1 -right-1 w-4 h-4 bg-emerald-400 rounded-full border-2 border-white"></div>
                            </div>
                            <div>
                                <h1 className="text-2xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
                                    AI Mentor
                                </h1>
                                <p className="text-sm text-gray-500">Персональная образовательная платформа</p>
                            </div>
                        </div>
                    </div>

                    <div className="flex items-center space-x-4">
                        <ConnectionIndicator />

                        <div className={`flex items-center space-x-3 px-6 py-3 rounded-full bg-gradient-to-r ${expertInfo.gradient} text-white shadow-lg`}>
                            <span className="text-2xl">{expertInfo.avatar}</span>
                            <div>
                                <div className="font-semibold text-sm">{expertInfo.name}</div>
                                <div className="text-xs text-white/80">{expertInfo.description}</div>
                            </div>
                        </div>

                        <div className="flex items-center space-x-2">
                            <button className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors">
                                <Settings className="w-5 h-5" />
                            </button>
                            <button className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors">
                                <LogOut className="w-5 h-5" />
                            </button>
                        </div>
                    </div>
                </div>
            </header>

            <div className="flex-1 flex overflow-hidden">
                {/* Enhanced Left Panel */}
                <div className="w-80 bg-white/70 backdrop-blur-lg border-r border-gray-200/50 flex flex-col">
                    {/* Progress Section */}
                    <div className="p-6 border-b border-gray-200/50">
                        <div className="flex items-center justify-between mb-6">
                            <h2 className="text-lg font-semibold text-gray-900">Прогресс</h2>
                            <div className="flex items-center space-x-2">
                                <Award className="w-5 h-5 text-amber-500" />
                                <span className="text-sm font-medium text-gray-700">{progressPercentage}%</span>
                            </div>
                        </div>

                        {/* Circular Progress */}
                        <div className="relative w-24 h-24 mx-auto mb-6">
                            <svg className="w-24 h-24 transform -rotate-90">
                                <circle
                                    cx="48"
                                    cy="48"
                                    r="40"
                                    stroke="currentColor"
                                    strokeWidth="8"
                                    fill="none"
                                    className="text-gray-200"
                                />
                                <circle
                                    cx="48"
                                    cy="48"
                                    r="40"
                                    stroke="currentColor"
                                    strokeWidth="8"
                                    fill="none"
                                    strokeDasharray={`${2 * Math.PI * 40}`}
                                    strokeDashoffset={`${2 * Math.PI * 40 * (1 - progressPercentage / 100)}`}
                                    className="text-indigo-600 transition-all duration-300"
                                    strokeLinecap="round"
                                />
                            </svg>
                            <div className="absolute inset-0 flex items-center justify-center">
                                <span className="text-2xl font-bold text-gray-900">{progressPercentage}%</span>
                            </div>
                        </div>

                        {/* Progress Details */}
                        <div className="space-y-3">
                            <div className="flex items-center justify-between text-sm">
                                <span className="text-gray-600">Пройденные темы</span>
                                <span className="font-medium">{Object.keys(studentData?.approved_topics || {}).length}</span>
                            </div>
                            <div className="flex items-center justify-between text-sm">
                                <span className="text-gray-600">Изученные блоки</span>
                                <span className="font-medium">{Object.keys(studentData?.approved_blocks || {}).length}</span>
                            </div>
                            <div className="flex items-center justify-between text-sm">
                                <span className="text-gray-600">Завершенные главы</span>
                                <span className="font-medium">{Object.keys(studentData?.approved_chapters || {}).length}</span>
                            </div>
                        </div>
                    </div>

                    {/* Current Learning */}
                    <div className="p-6 flex-1">
                        <h3 className="text-md font-semibold text-gray-900 mb-4">Текущее обучение</h3>

                        <div className="space-y-4">
                            {studentData?.current_topic && (
                                <div className="p-4 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl border border-blue-200/50">
                                    <div className="flex items-center space-x-3">
                                        <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                                            <BookOpen className="w-5 h-5 text-blue-600" />
                                        </div>
                                        <div className="flex-1">
                                            <div className="text-sm font-medium text-gray-900">Тема</div>
                                            <div className="text-sm text-gray-600">
                                                {Object.values(studentData.current_topic)[0]}
                                            </div>
                                        </div>
                                        <ChevronRight className="w-4 h-4 text-gray-400" />
                                    </div>
                                </div>
                            )}

                            {studentData?.current_block && (
                                <div className="p-4 bg-gradient-to-r from-emerald-50 to-teal-50 rounded-xl border border-emerald-200/50">
                                    <div className="flex items-center space-x-3">
                                        <div className="w-10 h-10 bg-emerald-100 rounded-lg flex items-center justify-center">
                                            <FileText className="w-5 h-5 text-emerald-600" />
                                        </div>
                                        <div className="flex-1">
                                            <div className="text-sm font-medium text-gray-900">Блок</div>
                                            <div className="text-sm text-gray-600">
                                                {Object.values(studentData.current_block)[0]}
                                            </div>
                                        </div>
                                        <ChevronRight className="w-4 h-4 text-gray-400" />
                                    </div>
                                </div>
                            )}

                            {studentData?.current_chapter && (
                                <div className="p-4 bg-gradient-to-r from-amber-50 to-orange-50 rounded-xl border border-amber-200/50">
                                    <div className="flex items-center space-x-3">
                                        <div className="w-10 h-10 bg-amber-100 rounded-lg flex items-center justify-center">
                                            <Play className="w-5 h-5 text-amber-600" />
                                        </div>
                                        <div className="flex-1">
                                            <div className="text-sm font-medium text-gray-900">Глава</div>
                                            <div className="text-sm text-gray-600">
                                                {Object.values(studentData.current_chapter)[0]}
                                            </div>
                                        </div>
                                        <ChevronRight className="w-4 h-4 text-gray-400" />
                                    </div>
                                </div>
                            )}
                        </div>
                    </div>

                    {/* Student Info */}
                    <div className="p-6 border-t border-gray-200/50 bg-gray-50/50">
                        <div className="text-sm space-y-2">
                            <div>
                                <span className="font-medium text-gray-700">Уровень:</span>
                                <span className="ml-2 text-gray-600">{studentData?.programming_experience || 'Не указан'}</span>
                            </div>
                            <div>
                                <span className="font-medium text-gray-700">Цель:</span>
                                <span className="ml-2 text-gray-600">{studentData?.learning_goals || 'Не указана'}</span>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Enhanced Chat Area */}
                <div className="flex-1 flex flex-col bg-white/30 backdrop-blur-sm">
                    <div className="flex-1 overflow-y-auto p-6" ref={chatContainerRef}>
                        <div className="max-w-4xl mx-auto space-y-6">
                            {messages.length === 0 && (
                                <div className="text-center py-12">
                                    <div className="w-16 h-16 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-full flex items-center justify-center mx-auto mb-4">
                                        <span className="text-2xl">👋</span>
                                    </div>
                                    <h3 className="text-xl font-semibold text-gray-900 mb-2">Добро пожаловать!</h3>
                                    <p className="text-gray-600">Начните диалог с вашим AI-ментором</p>
                                </div>
                            )}

                            {messages.map((message) => (
                                <div key={message.id} className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                                    <div className={`max-w-3xl ${message.role === 'user' ? 'order-1' : 'order-2'}`}>
                                        <div className={`rounded-2xl px-6 py-4 shadow-lg ${
                                            message.role === 'user'
                                                ? 'bg-gradient-to-r from-indigo-500 to-purple-600 text-white ml-12'
                                                : message.isError
                                                    ? 'bg-gradient-to-r from-red-50 to-red-100 text-red-800 border border-red-200 mr-12'
                                                    : 'bg-white text-gray-900 border border-gray-200/50 mr-12'
                                        }`}>
                                            <div className="whitespace-pre-wrap leading-relaxed">{message.text}</div>

                                            {message.commands && message.commands.length > 0 && (
                                                <div className="mt-3 pt-3 border-t border-gray-200/50">
                                                    <div className="text-xs text-gray-500 mb-2">Выполненные действия:</div>
                                                    <div className="space-y-1">
                                                        {message.commands.map((cmd, idx) => (
                                                            <div key={idx} className="text-xs bg-gray-50 px-2 py-1 rounded">
                                                                {cmd.description}
                                                            </div>
                                                        ))}
                                                    </div>
                                                </div>
                                            )}

                                            <div className={`text-xs mt-3 ${
                                                message.role === 'user' ? 'text-indigo-100' : 'text-gray-500'
                                            }`}>
                                                {new Date(message.timestamp).toLocaleTimeString()}
                                            </div>
                                        </div>
                                    </div>

                                    <div className={`w-10 h-10 rounded-full flex items-center justify-center shadow-md ${
                                        message.role === 'user'
                                            ? 'bg-gradient-to-r from-indigo-500 to-purple-600 text-white order-2 ml-3'
                                            : `bg-gradient-to-r ${expertInfo.gradient} text-white order-1 mr-3`
                                    }`}>
                                        {message.role === 'user' ? '👤' : expertInfo.avatar}
                                    </div>
                                </div>
                            ))}

                            {loading && (
                                <div className="flex justify-start">
                                    <div className="flex items-center space-x-3">
                                        <div className={`w-10 h-10 rounded-full bg-gradient-to-r ${expertInfo.gradient} text-white flex items-center justify-center shadow-md`}>
                                            {expertInfo.avatar}
                                        </div>
                                        <div className="bg-white text-gray-900 border border-gray-200/50 rounded-2xl px-6 py-4 shadow-lg">
                                            <div className="flex items-center space-x-3">
                                                <div className="flex space-x-1">
                                                    <div className="w-2 h-2 bg-indigo-500 rounded-full animate-bounce"></div>
                                                    <div className="w-2 h-2 bg-indigo-500 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                                                    <div className="w-2 h-2 bg-indigo-500 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                                                </div>
                                                <span className="text-sm text-gray-600">{expertInfo.name} печатает...</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            )}

                            <div ref={messagesEndRef} />
                        </div>
                    </div>

                    {/* Enhanced Input Area */}
                    <div className="border-t border-gray-200/50 bg-white/80 backdrop-blur-lg p-6">
                        <div className="max-w-4xl mx-auto">
                            <div className="flex space-x-4 items-end">
                                <div className="flex-1">
                                    <div className="relative">
                    <textarea
                        value={inputText}
                        onChange={(e) => setInputText(e.target.value)}
                        onKeyPress={handleKeyPress}
                        placeholder="Напишите ваше сообщение..."
                        className="w-full px-6 py-4 pr-12 border border-gray-300 rounded-2xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-none shadow-sm bg-white/90 backdrop-blur-sm"
                        rows="2"
                        disabled={loading}
                    />
                                        <button
                                            onClick={() => setIsRecording(!isRecording)}
                                            className={`absolute right-3 top-3 p-2 rounded-lg transition-colors ${
                                                isRecording
                                                    ? 'bg-red-500 text-white'
                                                    : 'text-gray-400 hover:text-gray-600 hover:bg-gray-100'
                                            }`}
                                        >
                                            {isRecording ? <MicOff className="w-4 h-4" /> : <Mic className="w-4 h-4" />}
                                        </button>
                                    </div>
                                </div>
                                <button
                                    onClick={sendMessage}
                                    disabled={!inputText.trim() || loading}
                                    className="px-8 py-4 bg-gradient-to-r from-indigo-500 to-purple-600 text-white rounded-2xl hover:from-indigo-600 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2 shadow-lg transition-all"
                                >
                                    <Send className="w-5 h-5" />
                                    <span className="font-medium">Отправить</span>
                                </button>
                            </div>

                            <div className="mt-3 flex items-center justify-between">
                                <div className="text-sm text-gray-600">
                                    {expertInfo.description}
                                </div>
                                <div className="flex items-center space-x-4 text-sm text-gray-500">
                                    <div className="flex items-center space-x-1">
                                        <Volume2 className="w-4 h-4" />
                                        <span>Озвучка</span>
                                    </div>
                                    <div>Enter для отправки</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Enhanced Content Panel */}
                <div className="w-96 bg-white/70 backdrop-blur-lg border-l border-gray-200/50 flex flex-col">
                    <div className="p-6 border-b border-gray-200/50">
                        <div className="flex items-center justify-between mb-4">
                            <h2 className="text-lg font-semibold text-gray-900">Материалы</h2>
                            <div className="flex items-center space-x-2">
                                <BookOpen className="w-5 h-5 text-indigo-600" />
                                <span className="text-sm text-gray-600">Контент</span>
                            </div>
                        </div>

                        {studentData?.current_chapter && (
                            <div className="text-sm text-gray-600 bg-gray-50 px-3 py-2 rounded-lg">
                                <span className="font-medium">Текущая глава:</span> {Object.values(studentData.current_chapter)[0]}
                            </div>
                        )}
                    </div>

                    <div className="flex-1 p-6 overflow-y-auto">
                        {studentData?.current_chapter ? (
                            <div className="space-y-4">
                                <div className="p-6 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl border border-blue-200/50">
                                    <div className="flex items-center space-x-3 mb-4">
                                        <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                                            <FileText className="w-6 h-6 text-blue-600" />
                                        </div>
                                        <div>
                                            <h3 className="font-semibold text-gray-900">Теоретический материал</h3>
                                            <p className="text-sm text-gray-600">Основы и концепции</p>
                                        </div>
                                    </div>
                                    <p className="text-sm text-gray-700 mb-4">
                                        Изучите основные принципы и теоретические аспекты текущей темы.
                                    </p>
                                    <button
                                        onClick={() => downloadContent('theory', Object.keys(studentData.current_chapter)[0])}
                                        className="w-full flex items-center justify-center space-x-2 bg-blue-600 text-white py-3 px-4 rounded-lg hover:bg-blue-700 transition-colors"
                                    >
                                        <Download className="w-4 h-4" />
                                        <span>Скачать материал</span>
                                    </button>
                                </div>

                                <div className="p-6 bg-gradient-to-br from-emerald-50 to-teal-50 rounded-xl border border-emerald-200/50">
                                    <div className="flex items-center space-x-3 mb-4">
                                        <div className="w-12 h-12 bg-emerald-100 rounded-lg flex items-center justify-center">
                                            <ClipboardCheck className="w-6 h-6 text-emerald-600" />
                                        </div>
                                        <div>
                                            <h3 className="font-semibold text-gray-900">Практические задания</h3>
                                            <p className="text-sm text-gray-600">Упражнения и проекты</p>
                                        </div>
                                    </div>
                                    <p className="text-sm text-gray-700 mb-4">
                                        Закрепите знания на практике с помощью специально подобранных заданий.
                                    </p>
                                    <button
                                        onClick={() => downloadContent('practice', Object.keys(studentData.current_chapter)[0])}
                                        className="w-full flex items-center justify-center space-x-2 bg-emerald-600 text-white py-3 px-4 rounded-lg hover:bg-emerald-700 transition-colors"
                                    >
                                        <Download className="w-4 h-4" />
                                        <span>Скачать задания</span>
                                    </button>
                                </div>

                                <div className="p-6 bg-gradient-to-br from-amber-50 to-orange-50 rounded-xl border border-amber-200/50">
                                    <div className="flex items-center space-x-3 mb-4">
                                        <div className="w-12 h-12 bg-amber-100 rounded-lg flex items-center justify-center">
                                            <Award className="w-6 h-6 text-amber-600" />
                                        </div>
                                        <div>
                                            <h3 className="font-semibold text-gray-900">Тестирование</h3>
                                            <p className="text-sm text-gray-600">Проверка знаний</p>
                                        </div>
                                    </div>
                                    <p className="text-sm text-gray-700 mb-4">
                                        Пройдите тест для оценки усвоения материала и получения сертификата.
                                    </p>
                                    <button className="w-full flex items-center justify-center space-x-2 bg-amber-600 text-white py-3 px-4 rounded-lg hover:bg-amber-700 transition-colors">
                                        <Play className="w-4 h-4" />
                                        <span>Начать тест</span>
                                    </button>
                                </div>
                            </div>
                        ) : (
                            <div className="text-center py-12">
                                <BookOpen className="w-16 h-16 mx-auto mb-4 text-gray-300" />
                                <h3 className="text-lg font-semibold text-gray-900 mb-2">Материалы не выбраны</h3>
                                <p className="text-gray-600">Начните диалог с ментором для выбора учебного материала</p>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default AIMentorPlatform;