import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import './features/onboarding/presentation/bloc/onboarding_bloc.dart';
import './features/onboarding/presentation/bloc/onboarding_state.dart';
import './core/theme/theme_cubit.dart';
import './core/theme/app_theme.dart';
import './core/theme/page_transitions.dart';
import './core/routes/app_routes.dart';
import './core/services/navigation_service.dart';
import './features/onboarding/presentation/screens/screen1_welcome.dart';
import './features/onboarding/presentation/screens/screen2_setup.dart';
import './features/onboarding/presentation/screens/screen3_personalized.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiBlocProvider(
      providers: [
        BlocProvider<ThemeCubit>(
          create: (context) => ThemeCubit(),
        ),
        BlocProvider<OnboardingBloc>(
          create: (context) => OnboardingBloc(),
        ),
      ],
      child: BlocBuilder<ThemeCubit, bool>(
        builder: (context, isDarkMode) {
          return MaterialApp(
            title: 'GoalMate',
            debugShowCheckedModeBanner: false,
            navigatorKey: NavigationService.navigatorKey,
            theme: isDarkMode ? AppTheme.darkTheme : AppTheme.lightTheme,
            initialRoute: AppRoutes.welcome,
            onGenerateRoute: (settings) {
              Widget page;
              switch (settings.name) {
                case AppRoutes.welcome:
                  page = const Screen1Welcome();
                  break;
                case AppRoutes.setup:
                  page = const Screen2Setup();
                  break;
                case AppRoutes.personalized:
                  page = const Screen3Personalized();
                  break;
                default:
                  page = const Screen1Welcome();
              }
              return PageTransitions.slideTransition(page);
            },
          );
        },
      ),
    );
  }
}
