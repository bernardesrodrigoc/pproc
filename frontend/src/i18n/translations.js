// Internationalization (i18n) for Editorial Decision Statistics Platform
// Supports: English (en), Portuguese (pt), Spanish (es)

const translations = {
  en: {
    // Navigation
    nav: {
      home: "Home",
      dashboard: "Dashboard",
      analytics: "Analytics",
      submit: "Submit Case",
      settings: "Settings",
      login: "Sign In",
      logout: "Sign Out",
      mySubmissions: "My Submissions"
    },
    // Landing Page
    landing: {
      heroTitle: "Transparency in Peer Review",
      heroSubtitle: "An anonymous, data-driven platform aggregating editorial decision statistics from scientific journals worldwide.",
      getStarted: "Get Started",
      exploreData: "Explore Data",
      trustedBy: "Trusted by researchers worldwide",
      howItWorks: "How It Works",
      step1Title: "Submit Anonymously",
      step1Desc: "Register your editorial decision with documentary evidence. Your identity is never revealed.",
      step2Title: "We Aggregate",
      step2Desc: "Data is processed into categorical statistics. No individual cases are ever displayed.",
      step3Title: "Explore Insights",
      step3Desc: "Access journal and publisher-level analytics to make informed submission decisions.",
      privacyTitle: "Privacy by Design",
      privacyDesc: "Your data is encrypted, anonymized, and never shared. We focus on process statistics, not individual complaints.",
      featuresTitle: "Platform Features",
      feature1: "Anonymous Submissions",
      feature2: "Encrypted Evidence Storage",
      feature3: "K-Anonymity Protection",
      feature4: "Multi-dimensional Scores",
      feature5: "Publisher Analytics",
      feature6: "Scientific Area Insights"
    },
    // Auth
    auth: {
      signInTitle: "Welcome Back",
      signInSubtitle: "Sign in to submit cases and track your contributions",
      signInWithGoogle: "Continue with Google",
      orcidLabel: "ORCID ID (Optional)",
      orcidPlaceholder: "0000-0000-0000-0000",
      privacyNote: "Your identity is protected. We only use your email for account access."
    },
    // Submission Form
    submission: {
      title: "Submit Editorial Decision",
      subtitle: "Help build transparency in peer review. All data is anonymized.",
      step1: "Manuscript",
      step2: "Journal",
      step3: "Decision",
      step4: "Review",
      step5: "Quality",
      step6: "Evidence",
      // Hierarchical Scientific Areas
      scientificAreaTitle: "Scientific Area",
      scientificAreaDesc: "Select your field of knowledge following the hierarchy",
      grandeArea: "Major Area",
      grandeAreaPlaceholder: "Select Major Area...",
      area: "Area",
      areaPlaceholder: "Select Area...",
      subarea: "Subarea (optional)",
      subareaPlaceholder: "Select Subarea (optional)...",
      // Legacy
      scientificArea: "Scientific Area",
      manuscriptType: "Manuscript Type",
      selectJournal: "Select Journal",
      selectPublisher: "Select Publisher",
      decisionType: "Decision Type",
      reviewerCount: "Number of Reviewers",
      timeToDecision: "Time to Decision",
      // Conditional: Open Access / APC
      journalOpenAccess: "Is the journal Open Access?",
      yes: "Yes",
      no: "No",
      apcRange: "Article Processing Charge",
      apcDesc: "Article Processing Charge (APC) charged by the journal",
      // Review Characteristics
      reviewComments: "Review Comment Types",
      reviewCommentsNote: "Note: For desk reject, this field can be empty.",
      editorComments: "Editor Provided Comments?",
      editorCommentsQuality: "Editor Comments Quality",
      editorCommentsQualityDesc: "How do you rate the quality of the editor's comments?",
      veryLow: "Very low",
      veryHigh: "Very high",
      perceivedCoherence: "Were comments compatible with your manuscript?",
      // Quality Assessment
      qualityAssessmentInfo: "These questions help build a comprehensive view of the editorial process. Your assessment contributes to understanding both positive and negative aspects.",
      overallReviewQuality: "Overall Review Quality",
      overallReviewQualityDesc: "How would you rate the overall quality of the peer review feedback?",
      feedbackClarity: "Feedback Clarity",
      feedbackClarityDesc: "How clear and actionable was the feedback provided?",
      decisionFairness: "Decision Fairness",
      decisionFairnessDesc: "Did the editorial decision align with the feedback received?",
      wouldRecommend: "Would Recommend",
      wouldRecommendDesc: "Based on the editorial process, would you recommend this journal to colleagues?",
      // Evidence
      uploadEvidence: "Upload Evidence",
      uploadDesc: "Upload the editorial decision email or screenshot. This file is encrypted and never public.",
      dragDrop: "Drag & drop or click to upload",
      supportedFormats: "PDF, PNG, JPG (max 10MB)",
      userAddedJournalNote: "User-added journals are stored as unverified until validation.",
      // Navigation
      next: "Continue",
      back: "Back",
      submit: "Submit",
      submitting: "Submitting...",
      successTitle: "Submission Received",
      successDesc: "Thank you for contributing to transparency in peer review.",
      privacyReminder: "Your submission is anonymous. The evidence you uploaded is encrypted and will only be used for internal validation."
    },
    // Dashboard
    dashboard: {
      title: "My Dashboard",
      welcomeBack: "Welcome back",
      mySubmissions: "My Submissions",
      noSubmissions: "You haven't submitted any cases yet.",
      startSubmitting: "Submit Your First Case",
      trustScore: "Trust Score",
      trustScoreDesc: "Based on your contribution history and consistency",
      contributions: "Contributions",
      recentActivity: "Recent Activity",
      status: {
        pending: "Pending Review",
        validated: "Validated",
        flagged: "Under Review"
      }
    },
    // Analytics
    analytics: {
      title: "Analytics Dashboard",
      subtitle: "Aggregated statistics from editorial decisions worldwide",
      overview: "Overview",
      publishers: "Publishers",
      journals: "Journals",
      areas: "Scientific Areas",
      totalSubmissions: "Total Submissions",
      avgTransparency: "Avg. Transparency",
      avgReviewDepth: "Avg. Review Depth",
      insufficientData: "Data collection in progress",
      dataCollectionTitle: "Aggregated Statistics — Data Collection in Progress",
      dataCollectionMessage: "To ensure statistical reliability and protect contributor anonymity, public metrics are published only when sufficient independent observations are available.",
      dataCollectionNote: "Your contribution has been recorded and will be included in aggregated analyses once publication thresholds are met.",
      dataCollectionWhyTitle: "Why this approach?",
      dataCollectionWhyList: [
        "Protects contributor identity through aggregation",
        "Ensures statistical robustness of published metrics",
        "Prevents identification of individual submissions"
      ],
      dataCollectionPersonalNote: "In the meantime, your Personal Insights dashboard displays analyses based exclusively on your own submissions.",
      scores: {
        transparency: "Transparency Index",
        transparencyDesc: "Measures reviewer presence and editorial engagement in the decision process",
        reviewDepth: "Review Depth Index",
        reviewDepthDesc: "Evaluates the thoroughness of peer review comments",
        editorialEffort: "Editorial Effort Index",
        editorialEffortDesc: "Assesses editor involvement with technical feedback",
        consistency: "Consistency Index",
        consistencyDesc: "Reflects alignment between review comments and manuscript content"
      },
      metrics: {
        deskRejectRate: "Desk Reject Rate",
        noPeerReviewRate: "No Peer Review Rate",
        fastDecisionRate: "Fast Decision Rate",
        slowDecisionRate: "Slow Decision Rate"
      },
      filterByPublisher: "Filter by Publisher",
      allPublishers: "All Publishers",
      cases: "cases"
    },
    // Settings
    settings: {
      title: "Settings",
      language: "Language",
      profile: "Profile",
      orcid: "ORCID ID",
      updateProfile: "Update Profile",
      saved: "Settings saved"
    },
    // Common
    common: {
      loading: "Loading...",
      error: "An error occurred",
      retry: "Retry",
      save: "Save",
      cancel: "Cancel",
      search: "Search",
      filter: "Filter",
      noResults: "No results found",
      learnMore: "Learn More"
    },
    // Footer
    footer: {
      tagline: "Building transparency in scientific publishing",
      terms: "Terms of Use",
      privacy: "Privacy Policy",
      about: "About",
      contact: "Contact"
    }
  },
  pt: {
    // Navigation
    nav: {
      home: "Início",
      dashboard: "Painel",
      analytics: "Análises",
      submit: "Enviar Caso",
      settings: "Configurações",
      login: "Entrar",
      logout: "Sair",
      mySubmissions: "Meus Envios"
    },
    // Landing Page
    landing: {
      heroTitle: "Transparência na Revisão por Pares",
      heroSubtitle: "Uma plataforma anônima e orientada por dados que agrega estatísticas de decisões editoriais de periódicos científicos em todo o mundo.",
      getStarted: "Começar",
      exploreData: "Explorar Dados",
      trustedBy: "Confiado por pesquisadores em todo o mundo",
      howItWorks: "Como Funciona",
      step1Title: "Envie Anonimamente",
      step1Desc: "Registre sua decisão editorial com evidência documental. Sua identidade nunca é revelada.",
      step2Title: "Nós Agregamos",
      step2Desc: "Os dados são processados em estatísticas categóricas. Nenhum caso individual é exibido.",
      step3Title: "Explore Insights",
      step3Desc: "Acesse análises de periódicos e editoras para tomar decisões informadas de submissão.",
      privacyTitle: "Privacidade por Design",
      privacyDesc: "Seus dados são criptografados, anonimizados e nunca compartilhados. Focamos em estatísticas de processo, não em reclamações individuais.",
      featuresTitle: "Recursos da Plataforma",
      feature1: "Envios Anônimos",
      feature2: "Armazenamento Criptografado",
      feature3: "Proteção K-Anonimato",
      feature4: "Pontuações Multidimensionais",
      feature5: "Análises de Editoras",
      feature6: "Insights por Área Científica"
    },
    // Auth
    auth: {
      signInTitle: "Bem-vindo de Volta",
      signInSubtitle: "Entre para enviar casos e acompanhar suas contribuições",
      signInWithGoogle: "Continuar com Google",
      orcidLabel: "ORCID ID (Opcional)",
      orcidPlaceholder: "0000-0000-0000-0000",
      privacyNote: "Sua identidade é protegida. Usamos seu email apenas para acesso à conta."
    },
    // Submission Form
    submission: {
      title: "Enviar Decisão Editorial",
      subtitle: "Ajude a construir transparência na revisão por pares. Todos os dados são anonimizados.",
      step1: "Manuscrito",
      step2: "Periódico",
      step3: "Decisão",
      step4: "Revisão",
      step5: "Qualidade",
      step6: "Evidência",
      // Hierarchical Scientific Areas
      scientificAreaTitle: "Área Científica",
      scientificAreaDesc: "Selecione sua área de conhecimento seguindo a hierarquia",
      grandeArea: "Grande Área",
      grandeAreaPlaceholder: "Selecione a Grande Área...",
      area: "Área",
      areaPlaceholder: "Selecione a Área...",
      subarea: "Subárea (opcional)",
      subareaPlaceholder: "Selecione a Subárea (opcional)...",
      // Legacy
      scientificArea: "Área Científica",
      manuscriptType: "Tipo de Manuscrito",
      selectJournal: "Selecionar Periódico",
      selectPublisher: "Selecionar Editora",
      decisionType: "Tipo de Decisão",
      reviewerCount: "Número de Revisores",
      timeToDecision: "Tempo até Decisão",
      // Conditional: Open Access / APC
      journalOpenAccess: "O periódico é Open Access?",
      yes: "Sim",
      no: "Não",
      apcRange: "Taxa de Processamento",
      apcDesc: "Taxa de Processamento de Artigo (APC) cobrada pelo periódico",
      // Review Characteristics
      reviewComments: "Tipos de Comentários da Revisão",
      reviewCommentsNote: "Nota: Para desk reject, este campo pode ficar vazio.",
      editorComments: "Editor Forneceu Comentários?",
      editorCommentsQuality: "Qualidade dos Comentários do Editor",
      editorCommentsQualityDesc: "Como você avalia a qualidade dos comentários fornecidos pelo editor?",
      veryLow: "Muito baixa",
      veryHigh: "Muito alta",
      perceivedCoherence: "Os comentários eram compatíveis com seu manuscrito?",
      // Quality Assessment
      qualityAssessmentInfo: "Estas perguntas ajudam a construir uma visão abrangente do processo editorial. Sua avaliação contribui para entender tanto aspectos positivos quanto negativos.",
      overallReviewQuality: "Qualidade Geral da Revisão",
      overallReviewQualityDesc: "Como você avalia a qualidade geral do feedback da revisão por pares?",
      feedbackClarity: "Clareza do Feedback",
      feedbackClarityDesc: "Quão claro e acionável foi o feedback fornecido?",
      decisionFairness: "Justiça da Decisão",
      decisionFairnessDesc: "A decisão editorial estava alinhada com o feedback recebido?",
      wouldRecommend: "Recomendaria",
      wouldRecommendDesc: "Com base no processo editorial, você recomendaria este periódico a colegas?",
      // Evidence
      uploadEvidence: "Enviar Evidência",
      uploadDesc: "Envie o email de decisão editorial ou captura de tela. Este arquivo é criptografado e nunca público.",
      dragDrop: "Arraste e solte ou clique para enviar",
      supportedFormats: "PDF, PNG, JPG (máx 10MB)",
      userAddedJournalNote: "Periódicos adicionados pelo usuário são armazenados como não verificados até validação.",
      // Navigation
      next: "Continuar",
      back: "Voltar",
      submit: "Enviar",
      submitting: "Enviando...",
      successTitle: "Envio Recebido",
      successDesc: "Obrigado por contribuir para a transparência na revisão por pares.",
      privacyReminder: "Seu envio é anônimo. A evidência que você enviou é criptografada e será usada apenas para validação interna."
    },
    // Dashboard
    dashboard: {
      title: "Meu Painel",
      welcomeBack: "Bem-vindo de volta",
      mySubmissions: "Meus Envios",
      noSubmissions: "Você ainda não enviou nenhum caso.",
      startSubmitting: "Enviar Seu Primeiro Caso",
      trustScore: "Pontuação de Confiança",
      trustScoreDesc: "Baseada no seu histórico de contribuições e consistência",
      contributions: "Contribuições",
      recentActivity: "Atividade Recente",
      status: {
        pending: "Em Análise",
        validated: "Validado",
        flagged: "Em Revisão"
      }
    },
    // Analytics
    analytics: {
      title: "Painel de Análises",
      subtitle: "Estatísticas agregadas de decisões editoriais em todo o mundo",
      overview: "Visão Geral",
      publishers: "Editoras",
      journals: "Periódicos",
      areas: "Áreas Científicas",
      totalSubmissions: "Total de Envios",
      avgTransparency: "Transparência Média",
      avgReviewDepth: "Profundidade Média",
      insufficientData: "Coleta de dados em andamento",
      dataCollectionTitle: "Estatísticas Agregadas — Coleta de Dados em Andamento",
      dataCollectionMessage: "Para garantir confiabilidade estatística e proteger o anonimato dos contribuidores, métricas públicas são publicadas apenas quando há observações independentes suficientes.",
      dataCollectionNote: "Sua contribuição foi registrada e será incluída nas análises agregadas assim que os limiares de publicação forem atingidos.",
      dataCollectionWhyTitle: "Por que essa abordagem?",
      dataCollectionWhyList: [
        "Protege a identidade dos contribuidores por meio de agregação",
        "Garante robustez estatística das métricas publicadas",
        "Previne a identificação de submissões individuais"
      ],
      dataCollectionPersonalNote: "Enquanto isso, seu painel de Insights Pessoais exibe análises baseadas exclusivamente em suas próprias submissões.",
      scores: {
        transparency: "Índice de Transparência",
        transparencyDesc: "Mede a presença de revisores e engajamento editorial no processo de decisão",
        reviewDepth: "Índice de Profundidade",
        reviewDepthDesc: "Avalia a minuciosidade dos comentários de revisão por pares",
        editorialEffort: "Índice de Esforço Editorial",
        editorialEffortDesc: "Avalia o envolvimento do editor com feedback técnico",
        consistency: "Índice de Consistência",
        consistencyDesc: "Reflete o alinhamento entre comentários de revisão e conteúdo do manuscrito"
      },
      metrics: {
        deskRejectRate: "Taxa de Rejeição Direta",
        noPeerReviewRate: "Taxa Sem Revisão",
        fastDecisionRate: "Taxa de Decisão Rápida",
        slowDecisionRate: "Taxa de Decisão Lenta"
      },
      filterByPublisher: "Filtrar por Editora",
      allPublishers: "Todas as Editoras",
      cases: "casos"
    },
    // Settings
    settings: {
      title: "Configurações",
      language: "Idioma",
      profile: "Perfil",
      orcid: "ORCID ID",
      updateProfile: "Atualizar Perfil",
      saved: "Configurações salvas"
    },
    // Common
    common: {
      loading: "Carregando...",
      error: "Ocorreu um erro",
      retry: "Tentar Novamente",
      save: "Salvar",
      cancel: "Cancelar",
      search: "Buscar",
      filter: "Filtrar",
      noResults: "Nenhum resultado encontrado",
      learnMore: "Saiba Mais"
    },
    // Footer
    footer: {
      tagline: "Construindo transparência na publicação científica",
      terms: "Termos de Uso",
      privacy: "Política de Privacidade",
      about: "Sobre",
      contact: "Contato"
    }
  },
  es: {
    // Navigation
    nav: {
      home: "Inicio",
      dashboard: "Panel",
      analytics: "Análisis",
      submit: "Enviar Caso",
      settings: "Configuración",
      login: "Iniciar Sesión",
      logout: "Cerrar Sesión",
      mySubmissions: "Mis Envíos"
    },
    // Landing Page
    landing: {
      heroTitle: "Transparencia en la Revisión por Pares",
      heroSubtitle: "Una plataforma anónima basada en datos que agrega estadísticas de decisiones editoriales de revistas científicas de todo el mundo.",
      getStarted: "Comenzar",
      exploreData: "Explorar Datos",
      trustedBy: "Confiado por investigadores de todo el mundo",
      howItWorks: "Cómo Funciona",
      step1Title: "Envía Anónimamente",
      step1Desc: "Registra tu decisión editorial con evidencia documental. Tu identidad nunca se revela.",
      step2Title: "Nosotros Agregamos",
      step2Desc: "Los datos se procesan en estadísticas categóricas. Ningún caso individual se muestra.",
      step3Title: "Explora Insights",
      step3Desc: "Accede a análisis de revistas y editoriales para tomar decisiones de envío informadas.",
      privacyTitle: "Privacidad por Diseño",
      privacyDesc: "Tus datos están encriptados, anonimizados y nunca se comparten. Nos enfocamos en estadísticas de proceso, no en quejas individuales.",
      featuresTitle: "Características de la Plataforma",
      feature1: "Envíos Anónimos",
      feature2: "Almacenamiento Encriptado",
      feature3: "Protección K-Anonimato",
      feature4: "Puntuaciones Multidimensionales",
      feature5: "Análisis de Editoriales",
      feature6: "Insights por Área Científica"
    },
    // Auth
    auth: {
      signInTitle: "Bienvenido de Nuevo",
      signInSubtitle: "Inicia sesión para enviar casos y seguir tus contribuciones",
      signInWithGoogle: "Continuar con Google",
      orcidLabel: "ORCID ID (Opcional)",
      orcidPlaceholder: "0000-0000-0000-0000",
      privacyNote: "Tu identidad está protegida. Solo usamos tu correo para acceso a la cuenta."
    },
    // Submission Form
    submission: {
      title: "Enviar Decisión Editorial",
      subtitle: "Ayuda a construir transparencia en la revisión por pares. Todos los datos son anonimizados.",
      step1: "Manuscrito",
      step2: "Revista",
      step3: "Decisión",
      step4: "Revisión",
      step5: "Calidad",
      step6: "Evidencia",
      // Hierarchical Scientific Areas
      scientificAreaTitle: "Área Científica",
      scientificAreaDesc: "Selecciona tu campo de conocimiento siguiendo la jerarquía",
      grandeArea: "Gran Área",
      grandeAreaPlaceholder: "Selecciona el Gran Área...",
      area: "Área",
      areaPlaceholder: "Selecciona el Área...",
      subarea: "Subárea (opcional)",
      subareaPlaceholder: "Selecciona la Subárea (opcional)...",
      // Legacy
      scientificArea: "Área Científica",
      manuscriptType: "Tipo de Manuscrito",
      selectJournal: "Seleccionar Revista",
      selectPublisher: "Seleccionar Editorial",
      decisionType: "Tipo de Decisión",
      reviewerCount: "Número de Revisores",
      timeToDecision: "Tiempo hasta Decisión",
      // Conditional: Open Access / APC
      journalOpenAccess: "¿La revista es Open Access?",
      yes: "Sí",
      no: "No",
      apcRange: "Cargo por Procesamiento",
      apcDesc: "Cargo por Procesamiento de Artículo (APC) cobrado por la revista",
      // Review Characteristics
      reviewComments: "Tipos de Comentarios de Revisión",
      reviewCommentsNote: "Nota: Para desk reject, este campo puede quedar vacío.",
      editorComments: "¿El Editor Proporcionó Comentarios?",
      editorCommentsQuality: "Calidad de los Comentarios del Editor",
      editorCommentsQualityDesc: "¿Cómo evalúas la calidad de los comentarios proporcionados por el editor?",
      veryLow: "Muy baja",
      veryHigh: "Muy alta",
      perceivedCoherence: "¿Los comentarios eran compatibles con tu manuscrito?",
      // Quality Assessment
      qualityAssessmentInfo: "Estas preguntas ayudan a construir una visión integral del proceso editorial. Tu evaluación contribuye a entender tanto aspectos positivos como negativos.",
      overallReviewQuality: "Calidad General de la Revisión",
      overallReviewQualityDesc: "¿Cómo evalúas la calidad general del feedback de la revisión por pares?",
      feedbackClarity: "Claridad del Feedback",
      feedbackClarityDesc: "¿Qué tan claro y accionable fue el feedback proporcionado?",
      decisionFairness: "Justicia de la Decisión",
      decisionFairnessDesc: "¿La decisión editorial estaba alineada con el feedback recibido?",
      wouldRecommend: "Recomendaría",
      wouldRecommendDesc: "Basándote en el proceso editorial, ¿recomendarías esta revista a colegas?",
      // Evidence
      uploadEvidence: "Subir Evidencia",
      uploadDesc: "Sube el correo de decisión editorial o captura de pantalla. Este archivo está encriptado y nunca es público.",
      dragDrop: "Arrastra y suelta o haz clic para subir",
      supportedFormats: "PDF, PNG, JPG (máx 10MB)",
      userAddedJournalNote: "Revistas añadidas por el usuario se almacenan como no verificadas hasta validación.",
      // Navigation
      next: "Continuar",
      back: "Volver",
      submit: "Enviar",
      submitting: "Enviando...",
      successTitle: "Envío Recibido",
      successDesc: "Gracias por contribuir a la transparencia en la revisión por pares.",
      privacyReminder: "Tu envío es anónimo. La evidencia que subiste está encriptada y solo se usará para validación interna."
    },
    // Dashboard
    dashboard: {
      title: "Mi Panel",
      welcomeBack: "Bienvenido de nuevo",
      mySubmissions: "Mis Envíos",
      noSubmissions: "Aún no has enviado ningún caso.",
      startSubmitting: "Enviar Tu Primer Caso",
      trustScore: "Puntuación de Confianza",
      trustScoreDesc: "Basada en tu historial de contribuciones y consistencia",
      contributions: "Contribuciones",
      recentActivity: "Actividad Reciente",
      status: {
        pending: "En Revisión",
        validated: "Validado",
        flagged: "Bajo Revisión"
      }
    },
    // Analytics
    analytics: {
      title: "Panel de Análisis",
      subtitle: "Estadísticas agregadas de decisiones editoriales de todo el mundo",
      overview: "Resumen",
      publishers: "Editoriales",
      journals: "Revistas",
      areas: "Áreas Científicas",
      totalSubmissions: "Total de Envíos",
      avgTransparency: "Transparencia Prom.",
      avgReviewDepth: "Profundidad Prom.",
      insufficientData: "Datos insuficientes para mostrar (mínimo 5 casos requeridos para k-anonimato)",
      scores: {
        transparency: "Índice de Transparencia",
        transparencyDesc: "Mide la presencia de revisores y compromiso editorial en el proceso de decisión",
        reviewDepth: "Índice de Profundidad",
        reviewDepthDesc: "Evalúa la minuciosidad de los comentarios de revisión por pares",
        editorialEffort: "Índice de Esfuerzo Editorial",
        editorialEffortDesc: "Evalúa la participación del editor con feedback técnico",
        consistency: "Índice de Consistencia",
        consistencyDesc: "Refleja la alineación entre comentarios de revisión y contenido del manuscrito"
      },
      metrics: {
        deskRejectRate: "Tasa de Rechazo Directo",
        noPeerReviewRate: "Tasa Sin Revisión",
        fastDecisionRate: "Tasa de Decisión Rápida",
        slowDecisionRate: "Tasa de Decisión Lenta"
      },
      filterByPublisher: "Filtrar por Editorial",
      allPublishers: "Todas las Editoriales",
      cases: "casos"
    },
    // Settings
    settings: {
      title: "Configuración",
      language: "Idioma",
      profile: "Perfil",
      orcid: "ORCID ID",
      updateProfile: "Actualizar Perfil",
      saved: "Configuración guardada"
    },
    // Common
    common: {
      loading: "Cargando...",
      error: "Ocurrió un error",
      retry: "Reintentar",
      save: "Guardar",
      cancel: "Cancelar",
      search: "Buscar",
      filter: "Filtrar",
      noResults: "No se encontraron resultados",
      learnMore: "Más Información"
    },
    // Footer
    footer: {
      tagline: "Construyendo transparencia en la publicación científica",
      terms: "Términos de Uso",
      privacy: "Política de Privacidad",
      about: "Acerca de",
      contact: "Contacto"
    }
  }
};

export default translations;
