import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { TextField, Button, Container, Typography, Box, Paper, Alert } from '@mui/material';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import axios from 'axios';
import { loginWithFirebase } from '../../firebase';

const Login = ({ login }) => {
    const [error, setError] = useState('');

    const formik = useFormik({
        initialValues: {
            email: '',
            password: '',
        },
        validationSchema: Yup.object({
            email: Yup.string().email('Invalid email address').required('Email is required'),
            password: Yup.string().required('Password is required'),
        }),
        onSubmit: async (values) => {
            try {
                setError(''); // Clear any previous errors

                // First, check if the API is accessible
                try {
                    // Try health check with longer timeout
                    const healthResponse = await axios.get('/api/health', {
                        timeout: 15000, // Further increase timeout to 15 seconds
                        // Don't throw error for status codes
                        validateStatus: () => true, // Accept any status code
                        // Don't send credentials for this check
                        withCredentials: false
                    });

                    // Log health check response
                    console.log('Health check response:', healthResponse.status, healthResponse.data);

                    // If health check returns error status, throw error
                    if (healthResponse.status >= 400) {
                        throw new Error(`Health check failed with status ${healthResponse.status}`);
                    }
                } catch (apiError) {
                    console.error('API connectivity error:', apiError);
                    throw new Error('Cannot connect to the backend server. Please check if the server is running and try again later.');
                }

                // Login with Firebase
                let firebaseToken;
                try {
                    const firebaseResult = await loginWithFirebase(values.email, values.password);
                    firebaseToken = firebaseResult.token;
                } catch (firebaseError) {
                    console.error('Firebase login error:', firebaseError);
                    // Try traditional login with email as username
                    try {
                        const res = await axios.post('/login/', {
                            username: values.email.split('@')[0], // Use part before @ as username
                            password: values.password
                        });

                        // Store token
                        localStorage.setItem('token', res.data.token);

                        // Call the app's login function to update state
                        login(res.data);
                        return true;
                    } catch (traditionalError) {
                        console.error('Traditional login error:', traditionalError);
                        // Check if it's a network error
                        if (traditionalError.message && traditionalError.message.includes('Network Error')) {
                            throw new Error('Cannot connect to the server. Please check your internet connection or try again later.');
                        }
                        // Both Firebase and traditional login failed
                        throw new Error(firebaseError.message || 'Authentication failed');
                    }
                }

                // If we get here, Firebase login succeeded
                // Login to our backend with Firebase token
                try {
                    const res = await axios.post('/login/', {
                        firebase_token: firebaseToken
                    });

                    // Store token
                    localStorage.setItem('token', res.data.token);

                    // Call the app's login function to update state
                    login(res.data);
                    return true;
                } catch (backendError) {
                    console.error('Backend login error:', backendError);
                    throw new Error('Login succeeded with Firebase but failed with our backend');
                }
            } catch (err) {
                setError(err.message || 'Invalid credentials. Please try again.');
                return false;
            }
        },
    });

    return (
        <Container maxWidth="sm">
            <Box sx={{ mt: 8, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                <Paper elevation={3} sx={{ p: 4, width: '100%' }}>
                    <Typography component="h1" variant="h5" align="center" gutterBottom>
                        Log In
                    </Typography>

                    {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

                    <Box component="form" onSubmit={formik.handleSubmit} sx={{ mt: 1 }}>
                        <TextField
                            margin="normal"
                            fullWidth
                            id="email"
                            label="Email Address"
                            name="email"
                            autoComplete="email"
                            autoFocus
                            value={formik.values.email}
                            onChange={formik.handleChange}
                            error={formik.touched.email && Boolean(formik.errors.email)}
                            helperText={formik.touched.email && formik.errors.email}
                        />
                        <TextField
                            margin="normal"
                            fullWidth
                            name="password"
                            label="Password"
                            type="password"
                            id="password"
                            autoComplete="current-password"
                            value={formik.values.password}
                            onChange={formik.handleChange}
                            error={formik.touched.password && Boolean(formik.errors.password)}
                            helperText={formik.touched.password && formik.errors.password}
                        />
                        <Button
                            type="submit"
                            fullWidth
                            variant="contained"
                            sx={{ mt: 3, mb: 2 }}
                            disabled={formik.isSubmitting}
                        >
                            {formik.isSubmitting ? 'Logging in...' : 'Log In'}
                        </Button>
                        <Box sx={{ mt: 2, textAlign: 'center' }}>
                            <Typography variant="body2">
                                Don't have an account?{' '}
                                <Link to="/register" style={{ textDecoration: 'none' }}>
                                    Register here
                                </Link>
                            </Typography>
                        </Box>
                    </Box>
                </Paper>
            </Box>
        </Container>
    );
};

export default Login; 