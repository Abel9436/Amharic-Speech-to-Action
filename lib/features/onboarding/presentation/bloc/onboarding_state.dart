import 'package:equatable/equatable.dart';

class OnboardingState extends Equatable {
  final String name;
  final String goal;
  final String? nameError;
  final String? goalError;
  final String? interestsError;
  final List<String> selectedInterests;
  final bool isLoading;
  final bool isFormValid;

  const OnboardingState({
    this.name = '',
    this.goal = '',
    this.nameError,
    this.goalError,
    this.interestsError,
    this.selectedInterests = const [],
    this.isLoading = false,
    this.isFormValid = false,
  });

  factory OnboardingState.initial() => const OnboardingState();

  OnboardingState copyWith({
    String? name,
    String? goal,
    String? nameError,
    String? goalError,
    String? interestsError,
    List<String>? selectedInterests,
    bool? isLoading,
    bool? isFormValid,
  }) {
    return OnboardingState(
      name: name ?? this.name,
      goal: goal ?? this.goal,
      nameError: nameError ?? this.nameError,
      goalError: goalError ?? this.goalError,
      interestsError: interestsError ?? this.interestsError,
      selectedInterests: selectedInterests ?? this.selectedInterests,
      isLoading: isLoading ?? this.isLoading,
      isFormValid: isFormValid ?? this.isFormValid,
    );
  }

  @override
  List<Object?> get props => [
        name,
        goal,
        nameError,
        goalError,
        interestsError,
        selectedInterests,
        isLoading,
        isFormValid
      ];
}
