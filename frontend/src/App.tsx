import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { RefreshCw, TrendingUp, AlertCircle } from 'lucide-react';

interface Signal {
  stock: string;
  event: string;
  sentiment: 'positive' | 'negative' | 'neutral';
  signal: 'buy' | 'sell' | 'hold';
  confidence: number;
  reason: string;
  headline: string;
  timestamp: string;
}

interface ApiResponse {
  signals: Signal[];
  count: number;
  timestamp: string;
}

const App: React.FC = () => {
  const [signals, setSignals] = useState<Signal[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>('');
  const [lastUpdated, setLastUpdated] = useState<string>('');
  const [filter, setFilter] = useState<'all' | 'buy' | 'sell' | 'hold'>('all');

  const fetchSignals = async () => {
    setLoading(true);
    setError('');
    
    try {
      const response = await axios.get<ApiResponse>('http://localhost:8000/signals', {
        timeout: 30000
      });
      setSignals(response.data.signals);
      setLastUpdated(new Date(response.data.timestamp).toLocaleTimeString());
    } catch (err: any) {
      if (err.code === 'ECONNABORTED') {
        setError('Request timed out. The analysis is taking longer than expected. Please try again.');
      } else {
        setError('Failed to fetch signals. Make sure the backend is running on localhost:8000');
      }
      console.error('Error fetching signals:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSignals();
    
    // Auto-refresh every 5 minutes
    const interval = setInterval(fetchSignals, 5 * 60 * 1000);
    return () => clearInterval(interval);
  }, []);

  const getSignalIcon = (signal: string) => {
    switch (signal) {
      case 'buy': return '🟢';
      case 'sell': return '🔴';
      case 'hold': return '⚪';
      default: return '⚫';
    }
  };

  const getSignalColor = (signal: string) => {
    switch (signal) {
      case 'buy': return 'text-green-600 bg-green-50 border-green-200';
      case 'sell': return 'text-red-600 bg-red-50 border-red-200';
      case 'hold': return 'text-gray-600 bg-gray-50 border-gray-200';
      default: return 'text-gray-600 bg-gray-50 border-gray-200';
    }
  };

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 80) return 'bg-green-500';
    if (confidence >= 60) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  const filteredSignals = signals.filter(signal => 
    filter === 'all' || signal.signal === filter
  );

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Stock News Analyzer
          </h1>
          <p className="text-gray-600">
            AI-powered analysis of stock news for trading signals
          </p>
          <div className="mt-2 text-sm text-gray-500">
            Real-time scraping from MoneyControl & Financial Express • AI analysis via Ollama
          </div>
        </div>

        {/* Controls */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
            <div className="flex gap-2">
              <button
                onClick={fetchSignals}
                disabled={loading}
                className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
              >
                <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
                {loading ? 'Analyzing...' : 'Refresh Signals'}
              </button>
              
              {/* Filter buttons */}
              <div className="flex gap-1">
                {['all', 'buy', 'sell', 'hold'].map((filterOption) => (
                  <button
                    key={filterOption}
                    onClick={() => setFilter(filterOption as any)}
                    className={`px-3 py-2 text-sm rounded-md capitalize ${
                      filter === filterOption
                        ? 'bg-blue-600 text-white'
                        : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                    }`}
                  >
                    {filterOption}
                  </button>
                ))}
              </div>
            </div>
            
            {lastUpdated && (
              <p className="text-sm text-gray-500">
                Last updated: {lastUpdated}
              </p>
            )}
          </div>
        </div>

        {/* Error display */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
            <div className="flex items-center gap-2">
              <AlertCircle className="w-5 h-5 text-red-600" />
              <p className="text-red-800">{error}</p>
            </div>
          </div>
        )}

        {/* Stats */}
        <div className="grid grid-cols-1 sm:grid-cols-4 gap-4 mb-6">
          <div className="bg-white rounded-lg shadow-md p-4">
            <h3 className="text-sm font-medium text-gray-500">Total Signals</h3>
            <p className="text-2xl font-bold text-gray-900">{filteredSignals.length}</p>
          </div>
          <div className="bg-white rounded-lg shadow-md p-4">
            <h3 className="text-sm font-medium text-gray-500">Buy Signals</h3>
            <p className="text-2xl font-bold text-green-600">
              {signals.filter(s => s.signal === 'buy').length}
            </p>
          </div>
          <div className="bg-white rounded-lg shadow-md p-4">
            <h3 className="text-sm font-medium text-gray-500">Sell Signals</h3>
            <p className="text-2xl font-bold text-red-600">
              {signals.filter(s => s.signal === 'sell').length}
            </p>
          </div>
          <div className="bg-white rounded-lg shadow-md p-4">
            <h3 className="text-sm font-medium text-gray-500">Hold Signals</h3>
            <p className="text-2xl font-bold text-gray-600">
              {signals.filter(s => s.signal === 'hold').length}
            </p>
          </div>
        </div>

        {/* Signals Grid */}
        {loading ? (
          <div className="flex justify-center items-center py-12">
            <RefreshCw className="w-8 h-8 animate-spin text-blue-600" />
            <span className="ml-2 text-gray-600">Loading signals...</span>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredSignals.map((signal, index) => (
              <div
                key={index}
                className={`bg-white rounded-lg shadow-md border-2 p-6 ${getSignalColor(signal.signal)}`}
              >
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h3 className="text-lg font-bold text-gray-900">
                      {signal.stock}
                    </h3>
                    <p className="text-sm text-gray-600">{signal.event}</p>
                  </div>
                  <div className="text-2xl">
                    {getSignalIcon(signal.signal)}
                    {signal.confidence >= 80 && <span className="ml-1">🔥</span>}
                  </div>
                </div>

                <div className="mb-4">
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-sm font-medium text-gray-700">
                      Confidence
                    </span>
                    <span className="text-sm font-bold">
                      {signal.confidence}%
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className={`h-2 rounded-full ${getConfidenceColor(signal.confidence)}`}
                      style={{ width: `${signal.confidence}%` }}
                    ></div>
                  </div>
                </div>

                <div className="mb-4">
                  <p className="text-sm text-gray-700">
                    <strong>Reason:</strong> {signal.reason}
                  </p>
                </div>

                <div className="mb-4">
                  <p className="text-xs text-gray-500 italic">
                    "{signal.headline}"
                  </p>
                </div>

                <div className="flex justify-between items-center text-xs text-gray-500">
                  <span className="capitalize">{signal.sentiment} sentiment</span>
                  <span>
                    {new Date(signal.timestamp).toLocaleTimeString()}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}

        {!loading && filteredSignals.length === 0 && !error && (
          <div className="text-center py-12">
            <TrendingUp className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-600">
              No signals found. Try refreshing to fetch new data.
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default App;