"""
Learning path generation service
"""

from typing import Dict, List, Any, Optional
import json
import logging
from utils.logger import get_logger
from core.gemini_client import GeminiClient

logger = get_logger(__name__)

class LearningPathGenerator:
    """Service for generating personalized learning paths"""
    
    def __init__(self):
        """Initialize learning path generator"""
        self.gemini_client = GeminiClient()
        
    def generate_learning_path(self, 
                             student_profile: Dict[str, Any], 
                             target_career: Dict[str, Any],
                             learning_preferences: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generate personalized learning path"""
        try:
            learning_path = {
                'student_profile': student_profile,
                'target_career': target_career,
                'learning_preferences': learning_preferences or {},
                'path_overview': {},
                'phases': [],
                'timeline': {},
                'resources': {},
                'milestones': [],
                'assessment_strategy': {},
                'ai_recommendations': {}
            }
            
            # Generate path overview
            learning_path['path_overview'] = self._generate_path_overview(student_profile, target_career)
            
            # Create learning phases
            learning_path['phases'] = self._create_learning_phases(student_profile, target_career)
            
            # Estimate timeline
            learning_path['timeline'] = self._estimate_learning_timeline(learning_path['phases'])
            
            # Gather resources
            learning_path['resources'] = self._gather_learning_resources(
                learning_path['phases'], learning_preferences
            )
            
            # Set milestones
            learning_path['milestones'] = self._set_learning_milestones(learning_path['phases'])
            
            # Create assessment strategy
            learning_path['assessment_strategy'] = self._create_assessment_strategy(
                student_profile, target_career
            )
            
            # Generate AI recommendations
            learning_path['ai_recommendations'] = self._generate_ai_recommendations(
                student_profile, target_career, learning_path['phases']
            )
            
            return learning_path
        except Exception as e:
            logger.error(f"Error generating learning path: {str(e)}")
            raise
    
    def adapt_learning_path(self, 
                           current_path: Dict[str, Any], 
                           progress_data: Dict[str, Any],
                           new_goals: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Adapt learning path based on progress and new goals"""
        try:
            adapted_path = current_path.copy()
            
            # Analyze progress
            progress_analysis = self._analyze_progress(progress_data)
            
            # Adjust phases based on progress
            adapted_path['phases'] = self._adjust_phases_based_on_progress(
                current_path['phases'], progress_analysis
            )
            
            # Update timeline
            adapted_path['timeline'] = self._update_timeline(
                adapted_path['phases'], progress_analysis
            )
            
            # Incorporate new goals
            if new_goals:
                adapted_path = self._incorporate_new_goals(adapted_path, new_goals)
            
            # Update recommendations
            adapted_path['ai_recommendations'] = self._generate_updated_recommendations(
                adapted_path, progress_analysis
            )
            
            return adapted_path
        except Exception as e:
            logger.error(f"Error adapting learning path: {str(e)}")
            raise
    
    def generate_career_specific_path(self, 
                                   career_id: str, 
                                   career_database: List[Dict[str, Any]],
                                   student_level: str = 'beginner') -> Dict[str, Any]:
        """Generate learning path for specific career"""
        try:
            # Find career in database
            career = next((c for c in career_database if c.get('id') == career_id), None)
            if not career:
                raise ValueError(f"Career with ID {career_id} not found")
            
            career_path = {
                'career': career,
                'student_level': student_level,
                'path_structure': {},
                'skill_requirements': [],
                'learning_modules': [],
                'certification_path': [],
                'practical_experience': [],
                'timeline': {},
                'resources': {}
            }
            
            # Analyze career requirements
            career_path['skill_requirements'] = self._analyze_career_requirements(career)
            
            # Create learning modules
            career_path['learning_modules'] = self._create_career_learning_modules(
                career, student_level
            )
            
            # Design certification path
            career_path['certification_path'] = self._design_certification_path(career)
            
            # Plan practical experience
            career_path['practical_experience'] = self._plan_practical_experience(career)
            
            # Estimate timeline
            career_path['timeline'] = self._estimate_career_timeline(
                career_path['learning_modules'], student_level
            )
            
            # Gather resources
            career_path['resources'] = self._gather_career_resources(career)
            
            return career_path
        except Exception as e:
            logger.error(f"Error generating career-specific path: {str(e)}")
            raise
    
    def create_skill_development_path(self, 
                                   skill: str, 
                                   current_level: str, 
                                   target_level: str,
                                   learning_style: str = 'visual') -> Dict[str, Any]:
        """Create focused skill development path"""
        try:
            skill_path = {
                'skill': skill,
                'current_level': current_level,
                'target_level': target_level,
                'learning_style': learning_style,
                'development_stages': [],
                'learning_resources': [],
                'practice_exercises': [],
                'assessment_methods': [],
                'timeline': {},
                'success_metrics': {}
            }
            
            # Create development stages
            skill_path['development_stages'] = self._create_skill_development_stages(
                skill, current_level, target_level
            )
            
            # Gather learning resources
            skill_path['learning_resources'] = self._gather_skill_resources(
                skill, learning_style
            )
            
            # Design practice exercises
            skill_path['practice_exercises'] = self._design_practice_exercises(
                skill, current_level, target_level
            )
            
            # Create assessment methods
            skill_path['assessment_methods'] = self._create_skill_assessments(
                skill, target_level
            )
            
            # Estimate timeline
            skill_path['timeline'] = self._estimate_skill_timeline(
                current_level, target_level
            )
            
            # Define success metrics
            skill_path['success_metrics'] = self._define_skill_success_metrics(
                skill, target_level
            )
            
            return skill_path
        except Exception as e:
            logger.error(f"Error creating skill development path: {str(e)}")
            raise
    
    def _generate_path_overview(self, 
                              student_profile: Dict[str, Any], 
                              target_career: Dict[str, Any]) -> Dict[str, Any]:
        """Generate learning path overview"""
        return {
            'path_name': f"Path to {target_career.get('title', 'Career')}",
            'estimated_duration': '6-12 months',
            'difficulty_level': self._assess_path_difficulty(student_profile, target_career),
            'learning_style': student_profile.get('learning_style', 'visual'),
            'current_skills': student_profile.get('skills', []),
            'target_skills': target_career.get('required_skills', []),
            'skill_gap': len(set(target_career.get('required_skills', [])) - set(student_profile.get('skills', []))),
            'path_summary': f"Comprehensive learning path to transition into {target_career.get('title', 'your target career')}"
        }
    
    def _create_learning_phases(self, 
                              student_profile: Dict[str, Any], 
                              target_career: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create learning phases"""
        phases = []
        
        # Phase 1: Foundation
        phases.append({
            'phase_name': 'Foundation',
            'duration': '1-2 months',
            'focus': 'Core concepts and fundamentals',
            'skills': self._get_foundation_skills(target_career),
            'learning_objectives': [
                'Understand basic concepts',
                'Develop fundamental skills',
                'Build learning habits'
            ],
            'deliverables': [
                'Complete foundation courses',
                'Build basic projects',
                'Pass foundation assessments'
            ]
        })
        
        # Phase 2: Intermediate
        phases.append({
            'phase_name': 'Intermediate',
            'duration': '2-4 months',
            'focus': 'Practical application and skill building',
            'skills': self._get_intermediate_skills(target_career),
            'learning_objectives': [
                'Apply skills in real projects',
                'Develop problem-solving abilities',
                'Build portfolio'
            ],
            'deliverables': [
                'Complete intermediate projects',
                'Build portfolio pieces',
                'Pass intermediate assessments'
            ]
        })
        
        # Phase 3: Advanced
        phases.append({
            'phase_name': 'Advanced',
            'duration': '2-4 months',
            'focus': 'Expertise development and specialization',
            'skills': self._get_advanced_skills(target_career),
            'learning_objectives': [
                'Master advanced concepts',
                'Develop specialization',
                'Prepare for career transition'
            ],
            'deliverables': [
                'Complete advanced projects',
                'Obtain certifications',
                'Build professional network'
            ]
        })
        
        return phases
    
    def _estimate_learning_timeline(self, phases: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Estimate learning timeline"""
        total_months = 0
        
        for phase in phases:
            duration = phase['duration']
            if '1-2' in duration:
                total_months += 1.5
            elif '2-4' in duration:
                total_months += 3
            elif '4-6' in duration:
                total_months += 5
        
        return {
            'total_duration': f"{total_months} months",
            'phases_count': len(phases),
            'estimated_start': 'Immediate',
            'estimated_completion': f"{total_months} months from start",
            'milestone_schedule': self._create_milestone_schedule(phases)
        }
    
    def _gather_learning_resources(self, 
                                 phases: List[Dict[str, Any]], 
                                 learning_preferences: Dict[str, Any]) -> Dict[str, List[Dict[str, str]]]:
        """Gather learning resources for each phase"""
        resources = {}
        
        for phase in phases:
            phase_name = phase['phase_name']
            resources[phase_name] = []
            
            for skill in phase['skills']:
                resources[phase_name].extend([
                    {
                        'type': 'Course',
                        'name': f'{skill} Course',
                        'url': f'https://example.com/courses/{skill.lower().replace(" ", "-")}',
                        'duration': '4-6 weeks',
                        'difficulty': 'beginner' if phase_name == 'Foundation' else 'intermediate'
                    },
                    {
                        'type': 'Book',
                        'name': f'Learn {skill}',
                        'url': f'https://example.com/books/{skill.lower().replace(" ", "-")}',
                        'duration': '2-3 weeks'
                    },
                    {
                        'type': 'Project',
                        'name': f'{skill} Project',
                        'url': f'https://example.com/projects/{skill.lower().replace(" ", "-")}',
                        'duration': '1-2 weeks'
                    }
                ])
        
        return resources
    
    def _set_learning_milestones(self, phases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Set learning milestones"""
        milestones = []
        
        for phase in phases:
            for deliverable in phase['deliverables']:
                milestones.append({
                    'milestone': deliverable,
                    'phase': phase['phase_name'],
                    'estimated_completion': phase['duration'],
                    'success_criteria': f"Complete {deliverable.lower()}",
                    'assessment_method': 'Project review' if 'project' in deliverable.lower() else 'Assessment test'
                })
        
        return milestones
    
    def _create_assessment_strategy(self, 
                                  student_profile: Dict[str, Any], 
                                  target_career: Dict[str, Any]) -> Dict[str, Any]:
        """Create assessment strategy"""
        return {
            'assessment_types': ['Formative', 'Summative', 'Peer Review', 'Self Assessment'],
            'assessment_frequency': 'Weekly',
            'assessment_methods': [
                'Multiple choice quizzes',
                'Practical projects',
                'Peer reviews',
                'Self-reflection journals'
            ],
            'passing_criteria': '80% or higher',
            'remediation_strategy': 'Additional practice and tutoring',
            'progress_tracking': 'Continuous monitoring with weekly reports'
        }
    
    def _generate_ai_recommendations(self, 
                                   student_profile: Dict[str, Any], 
                                   target_career: Dict[str, Any],
                                   phases: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate AI recommendations"""
        try:
            recommendations = self.gemini_client.generate_learning_recommendations(
                [target_career.get('title', '')],
                student_profile.get('skills', []),
                student_profile.get('learning_style', 'visual')
            )
            
            return recommendations
        except Exception as e:
            logger.error(f"Error generating AI recommendations: {str(e)}")
            return {}
    
    def _analyze_progress(self, progress_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze learning progress"""
        return {
            'completed_phases': progress_data.get('completed_phases', []),
            'completed_milestones': progress_data.get('completed_milestones', []),
            'skill_progress': progress_data.get('skill_progress', {}),
            'time_spent': progress_data.get('time_spent', 0),
            'performance_scores': progress_data.get('performance_scores', {}),
            'challenges_faced': progress_data.get('challenges_faced', [])
        }
    
    def _adjust_phases_based_on_progress(self, 
                                       phases: List[Dict[str, Any]], 
                                       progress_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Adjust phases based on progress"""
        adjusted_phases = []
        
        for phase in phases:
            if phase['phase_name'] not in progress_analysis['completed_phases']:
                # Adjust phase based on progress
                if progress_analysis['performance_scores'].get(phase['phase_name'], 0) > 80:
                    # Accelerate phase
                    phase['duration'] = self._reduce_duration(phase['duration'])
                elif progress_analysis['performance_scores'].get(phase['phase_name'], 0) < 60:
                    # Extend phase
                    phase['duration'] = self._extend_duration(phase['duration'])
                
                adjusted_phases.append(phase)
        
        return adjusted_phases
    
    def _update_timeline(self, 
                       phases: List[Dict[str, Any]], 
                       progress_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Update timeline based on progress"""
        return self._estimate_learning_timeline(phases)
    
    def _incorporate_new_goals(self, 
                             learning_path: Dict[str, Any], 
                             new_goals: Dict[str, Any]) -> Dict[str, Any]:
        """Incorporate new goals into learning path"""
        # Add new skills to phases
        if 'new_skills' in new_goals:
            for phase in learning_path['phases']:
                phase['skills'].extend(new_goals['new_skills'])
        
        # Add new milestones
        if 'new_milestones' in new_goals:
            learning_path['milestones'].extend(new_goals['new_milestones'])
        
        return learning_path
    
    def _generate_updated_recommendations(self, 
                                       learning_path: Dict[str, Any], 
                                       progress_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate updated recommendations"""
        return {
            'performance_insights': 'Good progress on foundation skills',
            'recommended_adjustments': [
                'Increase practice time for challenging skills',
                'Seek additional resources for advanced topics'
            ],
            'next_focus_areas': [
                'Complete current phase milestones',
                'Begin preparation for next phase'
            ]
        }
    
    def _analyze_career_requirements(self, career: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze career requirements"""
        requirements = []
        
        # Education requirements
        if career.get('education_requirements'):
            requirements.append({
                'type': 'Education',
                'requirement': career['education_requirements'],
                'importance': 'High',
                'alternatives': ['Relevant experience', 'Certifications']
            })
        
        # Skill requirements
        for skill in career.get('required_skills', []):
            requirements.append({
                'type': 'Skill',
                'requirement': skill,
                'importance': 'High',
                'alternatives': ['Transferable skills', 'Training programs']
            })
        
        # Experience requirements
        if career.get('experience_required'):
            requirements.append({
                'type': 'Experience',
                'requirement': career.get('experience_required'),
                'importance': 'Medium',
                'alternatives': ['Internships', 'Volunteer work', 'Projects']
            })
        
        return requirements
    
    def _create_career_learning_modules(self, 
                                      career: Dict[str, Any], 
                                      student_level: str) -> List[Dict[str, Any]]:
        """Create career-specific learning modules"""
        modules = []
        
        # Core skills module
        modules.append({
            'module_name': 'Core Skills',
            'skills': career.get('required_skills', [])[:5],  # Top 5 skills
            'duration': '2-3 months',
            'difficulty': 'beginner' if student_level == 'beginner' else 'intermediate',
            'learning_objectives': [
                'Master core technical skills',
                'Understand industry standards',
                'Build practical experience'
            ]
        })
        
        # Industry knowledge module
        modules.append({
            'module_name': 'Industry Knowledge',
            'skills': ['Industry trends', 'Market analysis', 'Regulatory knowledge'],
            'duration': '1-2 months',
            'difficulty': 'beginner',
            'learning_objectives': [
                'Understand industry landscape',
                'Learn market dynamics',
                'Stay updated with trends'
            ]
        })
        
        # Professional skills module
        modules.append({
            'module_name': 'Professional Skills',
            'skills': ['Communication', 'Project management', 'Leadership'],
            'duration': '1-2 months',
            'difficulty': 'intermediate',
            'learning_objectives': [
                'Develop professional communication',
                'Learn project management',
                'Build leadership skills'
            ]
        })
        
        return modules
    
    def _design_certification_path(self, career: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Design certification path"""
        certifications = []
        
        # Industry certifications
        if career.get('certifications'):
            for cert in career['certifications']:
                certifications.append({
                    'certification': cert,
                    'provider': 'Industry Association',
                    'duration': '3-6 months',
                    'prerequisites': 'Basic knowledge',
                    'cost': '$500-1000',
                    'validity': '2-3 years'
                })
        
        # Professional certifications
        certifications.extend([
            {
                'certification': 'Professional Certification',
                'provider': 'Professional Body',
                'duration': '6-12 months',
                'prerequisites': 'Experience required',
                'cost': '$1000-2000',
                'validity': '3-5 years'
            }
        ])
        
        return certifications
    
    def _plan_practical_experience(self, career: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Plan practical experience opportunities"""
        experiences = []
        
        experiences.extend([
            {
                'type': 'Internship',
                'description': f'Gain hands-on experience in {career.get("title", "field")}',
                'duration': '3-6 months',
                'requirements': 'Basic knowledge',
                'benefits': ['Real-world experience', 'Industry connections', 'Skill development']
            },
            {
                'type': 'Project Work',
                'description': 'Complete industry-relevant projects',
                'duration': '1-3 months',
                'requirements': 'Intermediate skills',
                'benefits': ['Portfolio building', 'Skill demonstration', 'Problem solving']
            },
            {
                'type': 'Volunteer Work',
                'description': 'Contribute to industry-related causes',
                'duration': 'Ongoing',
                'requirements': 'Basic skills',
                'benefits': ['Networking', 'Skill practice', 'Community impact']
            }
        ])
        
        return experiences
    
    def _estimate_career_timeline(self, 
                                learning_modules: List[Dict[str, Any]], 
                                student_level: str) -> Dict[str, Any]:
        """Estimate career-specific timeline"""
        total_months = 0
        
        for module in learning_modules:
            duration = module['duration']
            if '1-2' in duration:
                total_months += 1.5
            elif '2-3' in duration:
                total_months += 2.5
            elif '3-6' in duration:
                total_months += 4.5
        
        # Adjust based on student level
        if student_level == 'beginner':
            total_months *= 1.5
        elif student_level == 'advanced':
            total_months *= 0.7
        
        return {
            'total_duration': f"{total_months} months",
            'modules_count': len(learning_modules),
            'estimated_completion': f"{total_months} months from start"
        }
    
    def _gather_career_resources(self, career: Dict[str, Any]) -> Dict[str, List[Dict[str, str]]]:
        """Gather career-specific resources"""
        return {
            'courses': [
                {
                    'name': f'{career.get("title")} Fundamentals',
                    'provider': 'Online Platform',
                    'url': f'https://example.com/courses/{career.get("id")}',
                    'duration': '4-6 weeks'
                }
            ],
            'books': [
                {
                    'name': f'Complete Guide to {career.get("title")}',
                    'author': 'Industry Expert',
                    'url': f'https://example.com/books/{career.get("id")}',
                    'pages': '300-400'
                }
            ],
            'tools': [
                {
                    'name': f'{career.get("title")} Software',
                    'type': 'Professional Tool',
                    'url': f'https://example.com/tools/{career.get("id")}',
                    'cost': 'Free/Paid'
                }
            ]
        }
    
    def _create_skill_development_stages(self, 
                                       skill: str, 
                                       current_level: str, 
                                       target_level: str) -> List[Dict[str, Any]]:
        """Create skill development stages"""
        stages = []
        
        level_progression = ['novice', 'beginner', 'intermediate', 'advanced', 'expert']
        current_index = level_progression.index(current_level) if current_level in level_progression else 0
        target_index = level_progression.index(target_level) if target_level in level_progression else len(level_progression) - 1
        
        for i in range(current_index, target_index):
            if i < len(level_progression) - 1:
                stages.append({
                    'stage': f"{level_progression[i].title()} to {level_progression[i + 1].title()}",
                    'current_level': level_progression[i],
                    'target_level': level_progression[i + 1],
                    'duration': self._get_stage_duration(level_progression[i], level_progression[i + 1]),
                    'focus_areas': self._get_stage_focus_areas(skill, level_progression[i + 1])
                })
        
        return stages
    
    def _gather_skill_resources(self, skill: str, learning_style: str) -> List[Dict[str, str]]:
        """Gather skill-specific resources"""
        resources = []
        
        # Course resources
        resources.append({
            'type': 'Course',
            'name': f'{skill} Course',
            'url': f'https://example.com/courses/{skill.lower().replace(" ", "-")}',
            'style': learning_style,
            'duration': '4-6 weeks'
        })
        
        # Practice resources
        resources.append({
            'type': 'Practice',
            'name': f'{skill} Practice Exercises',
            'url': f'https://example.com/practice/{skill.lower().replace(" ", "-")}',
            'style': 'hands-on',
            'duration': 'ongoing'
        })
        
        # Community resources
        resources.append({
            'type': 'Community',
            'name': f'{skill} Community',
            'url': f'https://example.com/community/{skill.lower().replace(" ", "-")}',
            'style': 'collaborative',
            'duration': 'ongoing'
        })
        
        return resources
    
    def _design_practice_exercises(self, 
                                 skill: str, 
                                 current_level: str, 
                                 target_level: str) -> List[Dict[str, Any]]:
        """Design practice exercises"""
        exercises = []
        
        # Beginner exercises
        if current_level in ['novice', 'beginner']:
            exercises.append({
                'exercise': f'Basic {skill} Exercise',
                'difficulty': 'beginner',
                'duration': '30-60 minutes',
                'description': f'Practice basic {skill} concepts',
                'resources': f'https://example.com/exercises/{skill.lower().replace(" ", "-")}-basic'
            })
        
        # Intermediate exercises
        if target_level in ['intermediate', 'advanced', 'expert']:
            exercises.append({
                'exercise': f'Intermediate {skill} Project',
                'difficulty': 'intermediate',
                'duration': '2-4 hours',
                'description': f'Build a {skill} project',
                'resources': f'https://example.com/projects/{skill.lower().replace(" ", "-")}-intermediate'
            })
        
        # Advanced exercises
        if target_level in ['advanced', 'expert']:
            exercises.append({
                'exercise': f'Advanced {skill} Challenge',
                'difficulty': 'advanced',
                'duration': '4-8 hours',
                'description': f'Solve complex {skill} problems',
                'resources': f'https://example.com/challenges/{skill.lower().replace(" ", "-")}-advanced'
            })
        
        return exercises
    
    def _create_skill_assessments(self, skill: str, target_level: str) -> List[Dict[str, Any]]:
        """Create skill assessments"""
        assessments = []
        
        assessments.extend([
            {
                'assessment': f'{skill} Knowledge Test',
                'type': 'Multiple Choice',
                'duration': '30 minutes',
                'passing_score': '80%',
                'frequency': 'After each module'
            },
            {
                'assessment': f'{skill} Practical Project',
                'type': 'Project-based',
                'duration': '2-4 hours',
                'passing_score': 'Satisfactory',
                'frequency': 'End of each phase'
            },
            {
                'assessment': f'{skill} Peer Review',
                'type': 'Peer Assessment',
                'duration': '1 hour',
                'passing_score': 'Positive feedback',
                'frequency': 'Monthly'
            }
        ])
        
        return assessments
    
    def _estimate_skill_timeline(self, current_level: str, target_level: str) -> Dict[str, Any]:
        """Estimate skill development timeline"""
        level_months = {
            'novice': 0,
            'beginner': 1,
            'intermediate': 3,
            'advanced': 6,
            'expert': 12
        }
        
        current_months = level_months.get(current_level, 0)
        target_months = level_months.get(target_level, 12)
        
        duration_months = target_months - current_months
        
        return {
            'duration': f"{duration_months} months",
            'current_level': current_level,
            'target_level': target_level,
            'estimated_completion': f"{duration_months} months from start"
        }
    
    def _define_skill_success_metrics(self, skill: str, target_level: str) -> Dict[str, Any]:
        """Define skill success metrics"""
        return {
            'knowledge_test_score': '80% or higher',
            'practical_project_completion': 'All projects completed successfully',
            'peer_review_rating': '4.0/5.0 or higher',
            'self_assessment_confidence': 'High confidence level',
            'industry_recognition': 'Positive feedback from professionals'
        }
    
    def _assess_path_difficulty(self, 
                              student_profile: Dict[str, Any], 
                              target_career: Dict[str, Any]) -> str:
        """Assess learning path difficulty"""
        current_skills = len(student_profile.get('skills', []))
        required_skills = len(target_career.get('required_skills', []))
        
        skill_gap = required_skills - current_skills
        
        if skill_gap <= 2:
            return 'easy'
        elif skill_gap <= 5:
            return 'medium'
        else:
            return 'hard'
    
    def _get_foundation_skills(self, target_career: Dict[str, Any]) -> List[str]:
        """Get foundation skills for career"""
        return target_career.get('required_skills', [])[:3]  # Top 3 skills
    
    def _get_intermediate_skills(self, target_career: Dict[str, Any]) -> List[str]:
        """Get intermediate skills for career"""
        skills = target_career.get('required_skills', [])
        return skills[3:6] if len(skills) > 3 else skills[3:]
    
    def _get_advanced_skills(self, target_career: Dict[str, Any]) -> List[str]:
        """Get advanced skills for career"""
        skills = target_career.get('required_skills', [])
        return skills[6:] if len(skills) > 6 else []
    
    def _create_milestone_schedule(self, phases: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Create milestone schedule"""
        schedule = []
        current_month = 0
        
        for phase in phases:
            duration = phase['duration']
            if '1-2' in duration:
                current_month += 1.5
            elif '2-4' in duration:
                current_month += 3
            elif '4-6' in duration:
                current_month += 5
            
            schedule.append({
                'milestone': f"Complete {phase['phase_name']}",
                'timeline': f"Month {current_month}"
            })
        
        return schedule
    
    def _reduce_duration(self, duration: str) -> str:
        """Reduce phase duration"""
        if '1-2' in duration:
            return '1 month'
        elif '2-4' in duration:
            return '1-2 months'
        elif '4-6' in duration:
            return '2-3 months'
        return duration
    
    def _extend_duration(self, duration: str) -> str:
        """Extend phase duration"""
        if '1-2' in duration:
            return '2-3 months'
        elif '2-4' in duration:
            return '4-6 months'
        elif '4-6' in duration:
            return '6-8 months'
        return duration
    
    def _get_stage_duration(self, current_level: str, target_level: str) -> str:
        """Get stage duration"""
        durations = {
            'novice': '1-2 months',
            'beginner': '2-3 months',
            'intermediate': '3-4 months',
            'advanced': '4-6 months',
            'expert': '6-12 months'
        }
        return durations.get(target_level, '2-3 months')
    
    def _get_stage_focus_areas(self, skill: str, level: str) -> List[str]:
        """Get stage focus areas"""
        focus_areas = {
            'beginner': ['Basic concepts', 'Fundamental skills', 'Simple applications'],
            'intermediate': ['Practical applications', 'Problem solving', 'Project building'],
            'advanced': ['Complex problems', 'Optimization', 'Best practices'],
            'expert': ['Innovation', 'Leadership', 'Teaching others']
        }
        return focus_areas.get(level, ['Skill development'])
