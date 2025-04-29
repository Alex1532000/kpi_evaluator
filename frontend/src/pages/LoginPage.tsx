import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Container,
  Paper,
  Typography,
  TextField,
  Button,
  FormControlLabel,
  Checkbox,
  Link,
  Grid,
  useTheme,
  useMediaQuery,
} from '@mui/material';
import { styled } from '@mui/material/styles';

// Componentes estilizados
const LoginContainer = styled(Box)(({ theme }) => ({
  minHeight: '100vh',
  display: 'flex',
  overflow: 'hidden',
}));

const ImageSection = styled(Box)(({ theme }) => ({
  flex: 2,
  background: `linear-gradient(135deg, ${theme.palette.primary.dark}, ${theme.palette.primary.main}, ${theme.palette.primary.light})`,
  display: 'flex',
  flexDirection: 'column',
  justifyContent: 'center',
  alignItems: 'center',
  padding: theme.spacing(4),
  color: 'white',
  position: 'relative',
}));

const LoginSection = styled(Box)(({ theme }) => ({
  flex: 1,
  display: 'flex',
  flexDirection: 'column',
  justifyContent: 'center',
  padding: theme.spacing(4),
  backgroundColor: theme.palette.background.default,
}));

const LoginBox = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(4),
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'stretch',
  borderRadius: 16,
  boxShadow: '0 4px 20px rgba(0,0,0,0.1)',
}));

const EvaluationIcon = styled(Typography)(({ theme }) => ({
  fontSize: '3rem',
  color: 'white',
  margin: theme.spacing(0, 2),
}));

const LoginPage = () => {
  const theme = useTheme();
  const navigate = useNavigate();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    remember: false,
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      // Aquí iría la llamada a la API
      console.log('Login attempt with:', formData);
      navigate('/dashboard');
    } catch (error) {
      console.error('Login failed:', error);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'remember' ? checked : value,
    }));
  };

  return (
    <LoginContainer>
      {!isMobile && (
        <ImageSection>
          <Typography variant="h3" sx={{ mb: 2, fontWeight: 'bold' }}>
            Evaluación de Desempeño
          </Typography>
          <Typography variant="h6" sx={{ mb: 4, maxWidth: '600px', textAlign: 'center' }}>
            Sistema integral para la gestión y evaluación del rendimiento laboral
          </Typography>
          <Box sx={{ display: 'flex', mb: 4 }}>
            <EvaluationIcon>📊</EvaluationIcon>
            <EvaluationIcon>📈</EvaluationIcon>
            <EvaluationIcon>🎯</EvaluationIcon>
          </Box>
          <Box
            component="img"
            src="https://img.freepik.com/free-vector/business-team-putting-together-jigsaw-puzzle-isolated-flat-vector-illustration-cartoon-partners-working-connection-teamwork-partnership-cooperation-concept_74855-9814.jpg"
            sx={{
              maxWidth: '80%',
              borderRadius: 2,
              boxShadow: '0 4px 20px rgba(0,0,0,0.2)',
            }}
          />
        </ImageSection>
      )}
      <LoginSection>
        <Container maxWidth="sm">
          <LoginBox>
            <Typography variant="h4" sx={{ mb: 1, textAlign: 'center' }}>
              Bienvenido
            </Typography>
            <Typography variant="body1" sx={{ mb: 4, textAlign: 'center', color: 'text.secondary' }}>
              Ingrese sus credenciales para continuar
            </Typography>
            <form onSubmit={handleSubmit}>
              <TextField
                fullWidth
                label="Usuario"
                name="username"
                value={formData.username}
                onChange={handleChange}
                margin="normal"
                variant="outlined"
                required
              />
              <TextField
                fullWidth
                label="Contraseña"
                name="password"
                type="password"
                value={formData.password}
                onChange={handleChange}
                margin="normal"
                variant="outlined"
                required
              />
              <FormControlLabel
                control={
                  <Checkbox
                    name="remember"
                    checked={formData.remember}
                    onChange={handleChange}
                    color="primary"
                  />
                }
                label="Recordar mis credenciales"
                sx={{ my: 2 }}
              />
              <Button
                type="submit"
                fullWidth
                variant="contained"
                size="large"
                sx={{ mb: 2 }}
              >
                Iniciar Sesión
              </Button>
              <Grid container justifyContent="center">
                <Grid item>
                  <Link href="#" variant="body2" color="primary">
                    ¿Olvidó su contraseña?
                  </Link>
                </Grid>
              </Grid>
            </form>
          </LoginBox>
        </Container>
      </LoginSection>
    </LoginContainer>
  );
};

export default LoginPage;
