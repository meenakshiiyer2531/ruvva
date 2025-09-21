"""
Mentor-student matching service
"""

from typing import Dict, List, Any, Optional, Tuple
import json
import logging
from utils.logger import get_logger
from core.cosine_matcher import CosineMatcher

logger = get_logger(__name__)

class MentorMatchingService:
    """Service for matching students with mentors"""
    
    def __init__(self):
        """Initialize mentor matching service"""
        self.cosine_matcher = CosineMatcher()
        
    def find_mentor_matches(self, 
                          student_profile: Dict[str, Any], 
                          mentor_database: List[Dict[str, Any]],
                          preferences: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Find mentor matches for student"""
        try:
            matches = {
                'student_profile': student_profile,
                'preferences': preferences or {},
                'mentor_matches': [],
                'matching_criteria': {},
                'recommendations': {},
                'next_steps': []
            }
            
            # Calculate mentor matches
            mentor_scores = []
            for mentor in mentor_database:
                match_score = self._calculate_mentor_match_score(student_profile, mentor)
                mentor_scores.append((mentor, match_score))
            
            # Sort by match score
            mentor_scores.sort(key=lambda x: x[1], reverse=True)
            
            # Apply preferences
            if preferences:
                mentor_scores = self._apply_mentor_preferences(mentor_scores, preferences)
            
            # Generate match details
            matches['mentor_matches'] = [
                {
                    'mentor': mentor,
                    'match_score': score,
                    'match_explanation': self._generate_match_explanation(student_profile, mentor),
                    'compatibility_factors': self._analyze_compatibility_factors(student_profile, mentor),
                    'recommended_approach': self._recommend_approach(student_profile, mentor)
                }
                for mentor, score in mentor_scores[:10]  # Top 10 matches
            ]
            
            # Analyze matching criteria
            matches['matching_criteria'] = self._analyze_matching_criteria(student_profile, mentor_scores[:5])
            
            # Generate recommendations
            matches['recommendations'] = self._generate_mentor_recommendations(student_profile, matches['mentor_matches'])
            
            # Suggest next steps
            matches['next_steps'] = self._suggest_mentor_next_steps(matches['mentor_matches'])
            
            return matches
        except Exception as e:
            logger.error(f"Error finding mentor matches: {str(e)}")
            raise
    
    def analyze_mentor_profile(self, 
                              mentor_id: str, 
                              mentor_database: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze detailed mentor profile"""
        try:
            # Find mentor in database
            mentor = next((m for m in mentor_database if m.get('id') == mentor_id), None)
            if not mentor:
                raise ValueError(f"Mentor with ID {mentor_id} not found")
            
            analysis = {
                'mentor': mentor,
                'profile_analysis': {},
                'expertise_areas': [],
                'mentoring_style': {},
                'availability': {},
                'success_metrics': {},
                'student_feedback': {},
                'recommendations': {}
            }
            
            # Analyze mentor profile
            analysis['profile_analysis'] = self._analyze_mentor_profile_details(mentor)
            
            # Extract expertise areas
            analysis['expertise_areas'] = self._extract_expertise_areas(mentor)
            
            # Analyze mentoring style
            analysis['mentoring_style'] = self._analyze_mentoring_style(mentor)
            
            # Check availability
            analysis['availability'] = self._check_mentor_availability(mentor)
            
            # Get success metrics
            analysis['success_metrics'] = self._get_mentor_success_metrics(mentor)
            
            # Get student feedback
            analysis['student_feedback'] = self._get_student_feedback(mentor)
            
            # Generate recommendations
            analysis['recommendations'] = self._generate_mentor_profile_recommendations(mentor)
            
            return analysis
        except Exception as e:
            logger.error(f"Error analyzing mentor profile: {str(e)}")
            raise
    
    def create_mentorship_plan(self, 
                            student_profile: Dict[str, Any], 
                            mentor_profile: Dict[str, Any],
                            goals: List[str]) -> Dict[str, Any]:
        """Create personalized mentorship plan"""
        try:
            mentorship_plan = {
                'student_profile': student_profile,
                'mentor_profile': mentor_profile,
                'goals': goals,
                'plan_overview': {},
                'sessions': [],
                'timeline': {},
                'milestones': [],
                'resources': {},
                'success_metrics': {}
            }
            
            # Create plan overview
            mentorship_plan['plan_overview'] = self._create_mentorship_overview(student_profile, mentor_profile, goals)
            
            # Design sessions
            mentorship_plan['sessions'] = self._design_mentorship_sessions(student_profile, mentor_profile, goals)
            
            # Create timeline
            mentorship_plan['timeline'] = self._create_mentorship_timeline(mentorship_plan['sessions'])
            
            # Set milestones
            mentorship_plan['milestones'] = self._set_mentorship_milestones(goals, mentorship_plan['sessions'])
            
            # Gather resources
            mentorship_plan['resources'] = self._gather_mentorship_resources(student_profile, mentor_profile)
            
            # Define success metrics
            mentorship_plan['success_metrics'] = self._define_mentorship_success_metrics(goals)
            
            return mentorship_plan
        except Exception as e:
            logger.error(f"Error creating mentorship plan: {str(e)}")
            raise
    
    def schedule_mentor_session(self, 
                              mentor_id: str, 
                              student_id: str,
                              session_type: str,
                              preferences: Dict[str, Any]) -> Dict[str, Any]:
        """Schedule mentor session"""
        try:
            session = {
                'session_id': f"{mentor_id}_{student_id}_{session_type}",
                'mentor_id': mentor_id,
                'student_id': student_id,
                'session_type': session_type,
                'preferences': preferences,
                'scheduling_options': [],
                'recommended_times': [],
                'session_preparation': {},
                'follow_up_plan': {}
            }
            
            # Generate scheduling options
            session['scheduling_options'] = self._generate_scheduling_options(mentor_id, preferences)
            
            # Recommend optimal times
            session['recommended_times'] = self._recommend_optimal_times(session['scheduling_options'])
            
            # Prepare session materials
            session['session_preparation'] = self._prepare_session_materials(session_type, preferences)
            
            # Plan follow-up
            session['follow_up_plan'] = self._plan_session_follow_up(session_type)
            
            return session
        except Exception as e:
            logger.error(f"Error scheduling mentor session: {str(e)}")
            raise
    
    def track_mentorship_progress(self, 
                                mentorship_id: str, 
                                progress_data: Dict[str, Any]) -> Dict[str, Any]:
        """Track mentorship progress"""
        try:
            progress_tracking = {
                'mentorship_id': mentorship_id,
                'progress_data': progress_data,
                'progress_analysis': {},
                'achievements': [],
                'challenges': [],
                'recommendations': [],
                'next_milestones': []
            }
            
            # Analyze progress
            progress_tracking['progress_analysis'] = self._analyze_mentorship_progress(progress_data)
            
            # Identify achievements
            progress_tracking['achievements'] = self._identify_mentorship_achievements(progress_data)
            
            # Identify challenges
            progress_tracking['challenges'] = self._identify_mentorship_challenges(progress_data)
            
            # Generate recommendations
            progress_tracking['recommendations'] = self._generate_progress_recommendations(progress_data)
            
            # Identify next milestones
            progress_tracking['next_milestones'] = self._identify_next_milestones(progress_data)
            
            return progress_tracking
        except Exception as e:
            logger.error(f"Error tracking mentorship progress: {str(e)}")
            raise
    
    def _calculate_mentor_match_score(self, 
                                   student_profile: Dict[str, Any], 
                                   mentor_profile: Dict[str, Any]) -> float:
        """Calculate mentor-student match score"""
        try:
            # Career alignment
            career_alignment = self._calculate_career_alignment(student_profile, mentor_profile)
            
            # Skill compatibility
            skill_compatibility = self._calculate_skill_compatibility(student_profile, mentor_profile)
            
            # Experience level match
            experience_match = self._calculate_experience_match(student_profile, mentor_profile)
            
            # Communication style match
            communication_match = self._calculate_communication_match(student_profile, mentor_profile)
            
            # Availability match
            availability_match = self._calculate_availability_match(student_profile, mentor_profile)
            
            # Weighted combination
            total_score = (
                career_alignment * 0.3 +
                skill_compatibility * 0.25 +
                experience_match * 0.2 +
                communication_match * 0.15 +
                availability_match * 0.1
            )
            
            return round(total_score, 3)
        except Exception as e:
            logger.error(f"Error calculating mentor match score: {str(e)}")
            return 0.0
    
    def _apply_mentor_preferences(self, 
                                mentor_scores: List[Tuple[Dict[str, Any], float]], 
                                preferences: Dict[str, Any]) -> List[Tuple[Dict[str, Any], float]]:
        """Apply student preferences to mentor matches"""
        filtered_scores = []
        
        for mentor, score in mentor_scores:
            include = True
            
            # Location preference
            if 'location' in preferences:
                mentor_location = mentor.get('location', '').lower()
                preferred_location = preferences['location'].lower()
                if preferred_location not in mentor_location:
                    include = False
            
            # Experience level preference
            if 'experience_level' in preferences:
                mentor_experience = mentor.get('experience_level', '').lower()
                preferred_experience = preferences['experience_level'].lower()
                if mentor_experience != preferred_experience:
                    include = False
            
            # Industry preference
            if 'industry' in preferences:
                mentor_industry = mentor.get('industry', '').lower()
                preferred_industry = preferences['industry'].lower()
                if preferred_industry not in mentor_industry:
                    include = False
            
            # Availability preference
            if 'availability' in preferences:
                mentor_availability = mentor.get('availability', {})
                preferred_availability = preferences['availability']
                if not self._check_availability_match(mentor_availability, preferred_availability):
                    include = False
            
            if include:
                filtered_scores.append((mentor, score))
        
        return filtered_scores
    
    def _generate_match_explanation(self, 
                                  student_profile: Dict[str, Any], 
                                  mentor_profile: Dict[str, Any]) -> str:
        """Generate explanation for mentor match"""
        explanations = []
        
        # Career alignment
        student_career_goals = student_profile.get('career_goals', [])
        mentor_expertise = mentor_profile.get('expertise_areas', [])
        
        if any(goal.lower() in ' '.join(mentor_experise).lower() for goal in student_career_goals):
            explanations.append("Strong career goal alignment")
        
        # Skill compatibility
        student_skills = [skill.lower() for skill in student_profile.get('skills', [])]
        mentor_skills = [skill.lower() for skill in mentor_profile.get('skills', [])]
        
        common_skills = set(student_skills) & set(mentor_skills)
        if common_skills:
            explanations.append(f"Shared skills: {', '.join(list(common_skills)[:3])}")
        
        # Experience level
        student_level = student_profile.get('experience_level', 'beginner')
        mentor_level = mentor_profile.get('experience_level', 'senior')
        
        if mentor_level in ['senior', 'expert'] and student_level in ['beginner', 'intermediate']:
            explanations.append("Appropriate experience level for guidance")
        
        return '; '.join(explanations) if explanations else "Good overall compatibility"
    
    def _analyze_compatibility_factors(self, 
                                     student_profile: Dict[str, Any], 
                                     mentor_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze compatibility factors"""
        return {
            'career_alignment': self._calculate_career_alignment(student_profile, mentor_profile),
            'skill_compatibility': self._calculate_skill_compatibility(student_profile, mentor_profile),
            'experience_match': self._calculate_experience_match(student_profile, mentor_profile),
            'communication_style': self._calculate_communication_match(student_profile, mentor_profile),
            'availability_match': self._calculate_availability_match(student_profile, mentor_profile),
            'personality_fit': self._calculate_personality_fit(student_profile, mentor_profile)
        }
    
    def _recommend_approach(self, 
                          student_profile: Dict[str, Any], 
                          mentor_profile: Dict[str, Any]) -> str:
        """Recommend approach for mentorship"""
        student_level = student_profile.get('experience_level', 'beginner')
        mentor_style = mentor_profile.get('mentoring_style', {})
        
        if student_level == 'beginner':
            return "Structured guidance with regular check-ins"
        elif student_level == 'intermediate':
            return "Collaborative approach with project-based learning"
        else:
            return "Peer-to-peer relationship with mutual learning"
    
    def _analyze_matching_criteria(self, 
                                 student_profile: Dict[str, Any], 
                                 top_matches: List[Tuple[Dict[str, Any], float]]) -> Dict[str, Any]:
        """Analyze matching criteria from top matches"""
        criteria_analysis = {
            'common_characteristics': [],
            'success_factors': [],
            'matching_patterns': []
        }
        
        # Analyze common characteristics
        industries = [match[0].get('industry') for match, _ in top_matches]
        experience_levels = [match[0].get('experience_level') for match, _ in top_matches]
        
        criteria_analysis['common_characteristics'] = [
            f"Industry: {max(set(industries), key=industries.count)}",
            f"Experience: {max(set(experience_levels), key=experience_levels.count)}"
        ]
        
        # Identify success factors
        criteria_analysis['success_factors'] = [
            "Career goal alignment",
            "Skill compatibility",
            "Appropriate experience level"
        ]
        
        return criteria_analysis
    
    def _generate_mentor_recommendations(self, 
                                       student_profile: Dict[str, Any], 
                                       mentor_matches: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate mentor recommendations"""
        return {
            'top_recommendation': mentor_matches[0] if mentor_matches else None,
            'alternative_options': mentor_matches[1:3] if len(mentor_matches) > 1 else [],
            'recommendation_reasons': [
                "Strong career alignment",
                "Appropriate experience level",
                "Good communication style match"
            ],
            'next_steps': [
                "Review mentor profiles in detail",
                "Schedule initial consultation",
                "Prepare questions for mentor"
            ]
        }
    
    def _suggest_mentor_next_steps(self, mentor_matches: List[Dict[str, Any]]) -> List[str]:
        """Suggest next steps for mentor matching"""
        steps = []
        
        if mentor_matches:
            steps.extend([
                "Review top mentor profiles",
                "Schedule informational interviews",
                "Prepare mentorship goals",
                "Create mentorship plan"
            ])
        else:
            steps.extend([
                "Expand search criteria",
                "Consider alternative mentor types",
                "Join professional networks",
                "Attend industry events"
            ])
        
        return steps
    
    def _analyze_mentor_profile_details(self, mentor: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze mentor profile details"""
        return {
            'experience_summary': f"{mentor.get('years_experience', 0)} years in {mentor.get('industry', 'various industries')}",
            'expertise_depth': len(mentor.get('expertise_areas', [])),
            'mentoring_experience': mentor.get('mentoring_experience', 'Not specified'),
            'communication_style': mentor.get('communication_style', 'Not specified'),
            'availability': mentor.get('availability', 'Not specified')
        }
    
    def _extract_expertise_areas(self, mentor: Dict[str, Any]) -> List[str]:
        """Extract mentor expertise areas"""
        return mentor.get('expertise_areas', [])
    
    def _analyze_mentoring_style(self, mentor: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze mentor's mentoring style"""
        return {
            'style': mentor.get('mentoring_style', 'collaborative'),
            'approach': mentor.get('mentoring_approach', 'structured'),
            'communication_preference': mentor.get('communication_preference', 'email'),
            'meeting_frequency': mentor.get('meeting_frequency', 'weekly'),
            'feedback_style': mentor.get('feedback_style', 'constructive')
        }
    
    def _check_mentor_availability(self, mentor: Dict[str, Any]) -> Dict[str, Any]:
        """Check mentor availability"""
        return {
            'current_load': mentor.get('current_mentees', 0),
            'max_capacity': mentor.get('max_mentees', 5),
            'available_slots': mentor.get('available_slots', []),
            'timezone': mentor.get('timezone', 'UTC'),
            'response_time': mentor.get('response_time', '24 hours')
        }
    
    def _get_mentor_success_metrics(self, mentor: Dict[str, Any]) -> Dict[str, Any]:
        """Get mentor success metrics"""
        return {
            'mentees_helped': mentor.get('mentees_helped', 0),
            'success_rate': mentor.get('success_rate', '85%'),
            'average_rating': mentor.get('average_rating', 4.5),
            'testimonials_count': mentor.get('testimonials_count', 0),
            'career_advancements': mentor.get('career_advancements', 0)
        }
    
    def _get_student_feedback(self, mentor: Dict[str, Any]) -> Dict[str, Any]:
        """Get student feedback for mentor"""
        return {
            'recent_feedback': mentor.get('recent_feedback', []),
            'common_praise': mentor.get('common_praise', []),
            'improvement_areas': mentor.get('improvement_areas', []),
            'overall_satisfaction': mentor.get('overall_satisfaction', 'high')
        }
    
    def _generate_mentor_profile_recommendations(self, mentor: Dict[str, Any]) -> Dict[str, Any]:
        """Generate recommendations based on mentor profile"""
        return {
            'best_for': [
                f"Students interested in {mentor.get('industry', 'various fields')}",
                f"Career level: {mentor.get('target_student_level', 'all levels')}",
                f"Learning style: {mentor.get('preferred_learning_style', 'flexible')}"
            ],
            'mentorship_approach': mentor.get('mentoring_approach', 'structured guidance'),
            'expected_outcomes': [
                "Career clarity and direction",
                "Skill development",
                "Professional network expansion"
            ]
        }
    
    def _create_mentorship_overview(self, 
                                  student_profile: Dict[str, Any], 
                                  mentor_profile: Dict[str, Any], 
                                  goals: List[str]) -> Dict[str, Any]:
        """Create mentorship overview"""
        return {
            'mentorship_name': f"Mentorship with {mentor_profile.get('name', 'Mentor')}",
            'duration': '3-6 months',
            'focus_areas': goals,
            'mentor_expertise': mentor_profile.get('expertise_areas', []),
            'student_goals': goals,
            'expected_outcomes': [
                "Achieve career goals",
                "Develop professional skills",
                "Build industry network"
            ]
        }
    
    def _design_mentorship_sessions(self, 
                                  student_profile: Dict[str, Any], 
                                  mentor_profile: Dict[str, Any], 
                                  goals: List[str]) -> List[Dict[str, Any]]:
        """Design mentorship sessions"""
        sessions = []
        
        # Initial session
        sessions.append({
            'session_number': 1,
            'session_type': 'Introduction',
            'duration': '60 minutes',
            'focus': 'Goal setting and relationship building',
            'preparation': [
                'Prepare career goals',
                'Review mentor background',
                'Prepare questions'
            ],
            'outcomes': [
                'Establish mentorship goals',
                'Create action plan',
                'Set expectations'
            ]
        })
        
        # Regular sessions
        for i, goal in enumerate(goals[:4]):  # Limit to 4 goals
            sessions.append({
                'session_number': i + 2,
                'session_type': 'Goal-focused',
                'duration': '45 minutes',
                'focus': f'Achieve goal: {goal}',
                'preparation': [
                    f'Prepare progress on {goal}',
                    'Identify challenges',
                    'Prepare questions'
                ],
                'outcomes': [
                    f'Make progress on {goal}',
                    'Receive guidance',
                    'Plan next steps'
                ]
            })
        
        # Final session
        sessions.append({
            'session_number': len(sessions) + 1,
            'session_type': 'Wrap-up',
            'duration': '60 minutes',
            'focus': 'Review progress and plan next steps',
            'preparation': [
                'Review all goals',
                'Prepare progress summary',
                'Plan future development'
            ],
            'outcomes': [
                'Review achievements',
                'Plan continued development',
                'Maintain relationship'
            ]
        })
        
        return sessions
    
    def _create_mentorship_timeline(self, sessions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create mentorship timeline"""
        return {
            'total_duration': f"{len(sessions)} sessions over 3-6 months",
            'session_frequency': 'Bi-weekly',
            'session_duration': '45-60 minutes',
            'timeline': [
                f"Session {session['session_number']}: {session['session_type']} - {session['focus']}"
                for session in sessions
            ]
        }
    
    def _set_mentorship_milestones(self, 
                                 goals: List[str], 
                                 sessions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Set mentorship milestones"""
        milestones = []
        
        for i, goal in enumerate(goals):
            milestones.append({
                'milestone': f"Progress on {goal}",
                'target_session': i + 2,
                'success_criteria': f"Demonstrate progress toward {goal}",
                'assessment_method': 'Mentor evaluation'
            })
        
        return milestones
    
    def _gather_mentorship_resources(self, 
                                   student_profile: Dict[str, Any], 
                                   mentor_profile: Dict[str, Any]) -> Dict[str, List[Dict[str, str]]]:
        """Gather mentorship resources"""
        return {
            'learning_materials': [
                {
                    'type': 'Industry Reports',
                    'name': f'{mentor_profile.get("industry", "Industry")} Reports',
                    'url': f'https://example.com/reports/{mentor_profile.get("industry", "").lower()}'
                }
            ],
            'tools': [
                {
                    'type': 'Communication Tool',
                    'name': 'Video Conferencing',
                    'url': 'https://example.com/video-tool'
                }
            ],
            'networking': [
                {
                    'type': 'Professional Network',
                    'name': f'{mentor_profile.get("industry", "Industry")} Network',
                    'url': f'https://example.com/network/{mentor_profile.get("industry", "").lower()}'
                }
            ]
        }
    
    def _define_mentorship_success_metrics(self, goals: List[str]) -> Dict[str, Any]:
        """Define mentorship success metrics"""
        return {
            'goal_achievement': f"{len(goals)} goals achieved",
            'skill_development': 'Measurable skill improvement',
            'career_progress': 'Career advancement or clarity',
            'relationship_quality': 'Positive mentor-student relationship',
            'network_expansion': 'Expanded professional network'
        }
    
    def _generate_scheduling_options(self, 
                                   mentor_id: str, 
                                   preferences: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate scheduling options"""
        return [
            {
                'date': 'Next week',
                'time_slots': ['9:00 AM', '2:00 PM', '4:00 PM'],
                'duration': '60 minutes',
                'format': 'Video call'
            },
            {
                'date': 'Following week',
                'time_slots': ['10:00 AM', '3:00 PM', '5:00 PM'],
                'duration': '60 minutes',
                'format': 'Video call'
            }
        ]
    
    def _recommend_optimal_times(self, scheduling_options: List[Dict[str, Any]]) -> List[str]:
        """Recommend optimal scheduling times"""
        return [
            'Tuesday 2:00 PM - Best for focused discussion',
            'Thursday 4:00 PM - Good for wrap-up conversations'
        ]
    
    def _prepare_session_materials(self, 
                                 session_type: str, 
                                 preferences: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare session materials"""
        return {
            'agenda': f'{session_type} session agenda',
            'preparation_checklist': [
                'Review goals',
                'Prepare questions',
                'Test technology'
            ],
            'materials': [
                'Career goals document',
                'Progress tracking sheet',
                'Questions list'
            ]
        }
    
    def _plan_session_follow_up(self, session_type: str) -> Dict[str, Any]:
        """Plan session follow-up"""
        return {
            'follow_up_tasks': [
                'Send session summary',
                'Schedule next session',
                'Update progress tracking'
            ],
            'next_steps': [
                'Complete assigned tasks',
                'Prepare for next session',
                'Reflect on learnings'
            ]
        }
    
    def _analyze_mentorship_progress(self, progress_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze mentorship progress"""
        return {
            'sessions_completed': progress_data.get('sessions_completed', 0),
            'goals_achieved': progress_data.get('goals_achieved', 0),
            'skill_improvement': progress_data.get('skill_improvement', {}),
            'overall_satisfaction': progress_data.get('satisfaction', 'high')
        }
    
    def _identify_mentorship_achievements(self, progress_data: Dict[str, Any]) -> List[str]:
        """Identify mentorship achievements"""
        achievements = []
        
        if progress_data.get('goals_achieved', 0) > 0:
            achievements.append(f"Achieved {progress_data['goals_achieved']} goals")
        
        if progress_data.get('skill_improvement', {}):
            achievements.append("Demonstrated skill improvement")
        
        return achievements
    
    def _identify_mentorship_challenges(self, progress_data: Dict[str, Any]) -> List[str]:
        """Identify mentorship challenges"""
        challenges = []
        
        if progress_data.get('sessions_completed', 0) < 3:
            challenges.append("Limited session attendance")
        
        if progress_data.get('goals_achieved', 0) == 0:
            challenges.append("No goals achieved yet")
        
        return challenges
    
    def _generate_progress_recommendations(self, progress_data: Dict[str, Any]) -> List[str]:
        """Generate progress recommendations"""
        recommendations = []
        
        if progress_data.get('sessions_completed', 0) < 3:
            recommendations.append("Increase session frequency")
        
        if progress_data.get('goals_achieved', 0) == 0:
            recommendations.append("Break down goals into smaller tasks")
        
        return recommendations
    
    def _identify_next_milestones(self, progress_data: Dict[str, Any]) -> List[str]:
        """Identify next milestones"""
        return [
            "Complete next goal",
            "Schedule next session",
            "Update progress tracking"
        ]
    
    def _calculate_career_alignment(self, 
                                  student_profile: Dict[str, Any], 
                                  mentor_profile: Dict[str, Any]) -> float:
        """Calculate career alignment score"""
        student_goals = [goal.lower() for goal in student_profile.get('career_goals', [])]
        mentor_expertise = [expertise.lower() for expertise in mentor_profile.get('expertise_areas', [])]
        
        if not student_goals or not mentor_expertise:
            return 0.5
        
        alignment_count = sum(1 for goal in student_goals 
                           if any(goal in expertise for expertise in mentor_expertise))
        
        return alignment_count / len(student_goals)
    
    def _calculate_skill_compatibility(self, 
                                     student_profile: Dict[str, Any], 
                                     mentor_profile: Dict[str, Any]) -> float:
        """Calculate skill compatibility score"""
        student_skills = [skill.lower() for skill in student_profile.get('skills', [])]
        mentor_skills = [skill.lower() for skill in mentor_profile.get('skills', [])]
        
        if not student_skills or not mentor_skills:
            return 0.5
        
        common_skills = set(student_skills) & set(mentor_skills)
        return len(common_skills) / len(student_skills)
    
    def _calculate_experience_match(self, 
                                  student_profile: Dict[str, Any], 
                                  mentor_profile: Dict[str, Any]) -> float:
        """Calculate experience level match"""
        student_level = student_profile.get('experience_level', 'beginner')
        mentor_level = mentor_profile.get('experience_level', 'senior')
        
        # Ideal: senior mentor for beginner/intermediate student
        if mentor_level in ['senior', 'expert'] and student_level in ['beginner', 'intermediate']:
            return 1.0
        elif mentor_level == 'mid' and student_level == 'beginner':
            return 0.8
        else:
            return 0.6
    
    def _calculate_communication_match(self, 
                                    student_profile: Dict[str, Any], 
                                    mentor_profile: Dict[str, Any]) -> float:
        """Calculate communication style match"""
        student_style = student_profile.get('communication_style', 'formal')
        mentor_style = mentor_profile.get('communication_style', 'friendly')
        
        if student_style == mentor_style:
            return 1.0
        else:
            return 0.7
    
    def _calculate_availability_match(self, 
                                    student_profile: Dict[str, Any], 
                                    mentor_profile: Dict[str, Any]) -> float:
        """Calculate availability match"""
        mentor_availability = mentor_profile.get('availability', {})
        
        if mentor_availability.get('current_mentees', 0) < mentor_availability.get('max_mentees', 5):
            return 1.0
        else:
            return 0.3
    
    def _calculate_personality_fit(self, 
                                 student_profile: Dict[str, Any], 
                                 mentor_profile: Dict[str, Any]) -> float:
        """Calculate personality fit"""
        # Simple heuristic based on mentoring style
        mentor_style = mentor_profile.get('mentoring_style', 'collaborative')
        student_preference = student_profile.get('preferred_mentoring_style', 'collaborative')
        
        if mentor_style == student_preference:
            return 1.0
        else:
            return 0.7
    
    def _check_availability_match(self, 
                               mentor_availability: Dict[str, Any], 
                               preferred_availability: Dict[str, Any]) -> bool:
        """Check if mentor availability matches preferences"""
        # Simple check for time overlap
        mentor_times = mentor_availability.get('available_times', [])
        preferred_times = preferred_availability.get('preferred_times', [])
        
        return bool(set(mentor_times) & set(preferred_times))
