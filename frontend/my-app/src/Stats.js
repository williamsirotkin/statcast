import React, { useState, useEffect } from 'react';
import { TextField, Button, Box, Typography } from '@mui/material';
import ApiClient from './ApiClient';

const api = new ApiClient('http://127.0.0.1:5000');

const StatBar = ({label, value, maxValue }) => {
    const percentage = Math.round((value / maxValue) * 100);
    return (
        <div style={{
            marginBottom: '20px',
            width: '100%'
          }}>
            <div style={{
              display: 'flex',
              justifyContent: 'space-between',
              marginBottom: '8px'
            }}>
              <span style={{ fontWeight: 'bold' }}>{label}</span>
              <span style={{ fontWeight: 'bold' }}>{value}</span>
            </div>
      
            <div style={{
              width: '100%',
              height: '30px',
              backgroundColor: '#e5e7eb',
              borderRadius: '4px',
              position: 'relative'
            }}>
              <div style={{
                position: 'absolute',
                left: 0,
                top: 0,
                width: `${percentage}%`,
                height: '100%',
                backgroundColor: '#dc2626',
                borderRadius: '4px'
              }} />
            </div>
          </div>
    );
};

const Stats = ({ player }) => {
    const [stats, setStats] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const getStats = async () => {
            try {
                setLoading(true);
                const data = await api.get('/getData/' + player);
                setStats(data);
                setError(null);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        if (player) {
            getStats();
        }
    }, [player]);

    if (loading) {
        return <div>Loading...</div>;
    }

    if (error) {
        return <div>Error: {error}</div>;
    }

    if (!stats) {
        return <div>No stats available</div>;
    }

    return (
        <div style={{
            display: 'flex',
            justifyContent: 'center',
            marginTop: '20px',
            padding: '20px'
        }}>
            <div style={{
                width: '500px',
                backgroundColor: 'white',
                padding: '30px',
                borderRadius: '8px',
                boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)'
            }}>
                {stats.map((stat, index) => (
                    <StatBar
                        key={index}
                        label={stat.label}
                        value={stat.value}
                        maxValue={100} 
                    />
                ))}
            </div>
        </div>
    );
};

export default Stats;