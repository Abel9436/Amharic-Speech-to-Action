import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:equatable/equatable.dart';
import '../../../../core/services/navigation_service.dart';
import '../../../../core/routes/app_routes.dart';
import 'onboarding_event.dart';
import 'onboarding_state.dart';

class OnboardingBloc extends Bloc<OnboardingEvent, OnboardingState> {
  OnboardingBloc() : super(OnboardingState.initial()) {
    on<StartPressed>((event, emit) {
      NavigationService.navigateTo(AppRoutes.setup);
    });
    on<BackPressed>((event, emit) {
      NavigationService.goBack();
    });
    on<NameChanged>((event, emit) {
      final name = event.name.trim();
      final newNameError = name.isEmpty ? 'Name required' : null;
      final isValidForm =
          _validateForm(name, state.goal, state.selectedInterests);

      emit(state.copyWith(
        name: name,
        nameError: newNameError,
        isFormValid: isValidForm,
      ));
    });
    on<GoalChanged>((event, emit) {
      final goal = event.goal.trim();
      final newGoalError = goal.isEmpty ? 'Goal required' : null;
      final isValidForm =
          _validateForm(state.name, goal, state.selectedInterests);

      emit(state.copyWith(
        goal: goal,
        goalError: newGoalError,
        isFormValid: isValidForm,
      ));
    });
    on<InterestToggled>((event, emit) {
      final interests = List<String>.from(state.selectedInterests);
      if (interests.contains(event.interest)) {
        interests.remove(event.interest);
      } else if (interests.length < 3) {
        interests.add(event.interest);
      }
      final newInterestsError =
          interests.length < 2 ? 'Select at least 2 interests' : null;
      final isValidForm = _validateForm(state.name, state.goal, interests);

      emit(state.copyWith(
        selectedInterests: interests,
        interestsError: newInterestsError,
        isFormValid: isValidForm,
      ));
    });
    on<SubmitProfile>((event, emit) async {
      // Re-validate all fields before attempting submission
      final newNameError = state.name.isEmpty ? 'Name required' : null;
      final newGoalError = state.goal.isEmpty ? 'Goal required' : null;
      final newInterestsError = state.selectedInterests.length < 2
          ? 'Select at least 2 interests'
          : null;

      final isValid = newNameError == null &&
          newGoalError == null &&
          newInterestsError == null;

      emit(state.copyWith(
        nameError: newNameError,
        goalError: newGoalError,
        interestsError: newInterestsError,
        isFormValid: isValid,
      ));

      if (isValid) {
        emit(state.copyWith(isLoading: true));
        await Future.delayed(const Duration(seconds: 2));
        emit(state.copyWith(isLoading: false));
        NavigationService.navigateTo(AppRoutes.personalized);
      } else {
        emit(state.copyWith(isLoading: false));
      }
    });
    on<CompleteOnboarding>((event, emit) {
      // Clear the entire navigation stack and go to home
      NavigationService.navigateToAndClearStack(AppRoutes.home);
    });
  }

  bool _validateForm(String name, String goal, List<String> interests) {
    return name.isNotEmpty && goal.isNotEmpty && interests.length >= 2;
  }
}
