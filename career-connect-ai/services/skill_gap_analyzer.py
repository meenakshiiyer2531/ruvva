"""
Skill gap analysis service
"""

from typing import Dict, List, Any, Optional, Tuple
import json
import logging
from utils.logger import get_logger
from core.gemini_client import GeminiClient

logger = get_logger(__name__)

class SkillGapAnalyzer:
    """Service for analyzing skill gaps and development needs"""
    
    def __init__(self):
        """Initialize skill gap analyzer"""
        self.gemini_client = GeminiClient()
        
    def analyze_skill_gaps(self, 
                          current_skills: List[str], 
                          target_career: Dict[str, Any],
                          student_profile: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Analyze skill gaps for career transition"""
        try:
            required_skills = target_career.get('required_skills', [])
            
            gap_analysis = {
                'current_skills': current_skills,
                'required_skills': required_skills,
                'skill_gaps': [],
                'transferable_skills': [],
                'skill_match_score': 0.0,
                'development_priorities': [],
                'learning_recommendations': {},
                'timeline_estimates': {},
                'ai_insights': {}
            }
            
            # Calculate skill gaps
            gap_analysis['skill_gaps'] = self._identify_skill_gaps(current_skills, required_skills)
            gap_analysis['transferable_skills'] = self._identify_transferable_skills(current_skills, required_skills)
            gap_analysis['skill_match_score'] = self._calculate_skill_match_score(current_skills, required_skills)
            
            # Prioritize skill development
            gap_analysis['development_priorities'] = self._prioritize_skill_development(
                gap_analysis['skill_gaps'], target_career
            )
            
            # Generate learning recommendations
            gap_analysis['learning_recommendations'] = self._generate_learning_recommendations(
                gap_analysis['skill_gaps'], target_career, student_profile
            )
            
            # Estimate timelines
            gap_analysis['timeline_estimates'] = self._estimate_learning_timelines(
                gap_analysis['skill_gaps'], target_career
            )
            
            # Generate AI insights
            gap_analysis['ai_insights'] = self._generate_skill_gap_insights(
                current_skills, required_skills, target_career
            )
            
            return gap_analysis
        except Exception as e:
            logger.error(f"Error analyzing skill gaps: {str(e)}")
            raise
    
    def compare_skill_sets(self, 
                          skills_a: List[str], 
                          skills_b: List[str]) -> Dict[str, Any]:
        """Compare two skill sets"""
        try:
            comparison = {
                'skills_a': skills_a,
                'skills_b': skills_b,
                'common_skills': [],
                'unique_to_a': [],
                'unique_to_b': [],
                'similarity_score': 0.0,
                'skill_overlap_percentage': 0.0
            }
            
            # Find common skills
            skills_a_lower = [skill.lower() for skill in skills_a]
            skills_b_lower = [skill.lower() for skill in skills_b]
            
            common_skills = set(skills_a_lower) & set(skills_b_lower)
            comparison['common_skills'] = list(common_skills)
            
            # Find unique skills
            comparison['unique_to_a'] = [skill for skill in skills_a_lower if skill not in skills_b_lower]
            comparison['unique_to_b'] = [skill for skill in skills_b_lower if skill not in skills_a_lower]
            
            # Calculate similarity
            total_skills = len(set(skills_a_lower) | set(skills_b_lower))
            if total_skills > 0:
                comparison['similarity_score'] = len(common_skills) / total_skills
                comparison['skill_overlap_percentage'] = (len(common_skills) / total_skills) * 100
            
            return comparison
        except Exception as e:
            logger.error(f"Error comparing skill sets: {str(e)}")
            raise
    
    def assess_skill_level(self, 
                          skill: str, 
                          evidence: List[str]) -> Dict[str, Any]:
        """Assess current skill level based on evidence"""
        try:
            assessment = {
                'skill': skill,
                'evidence': evidence,
                'skill_level': 'beginner',
                'confidence_score': 0.0,
                'assessment_factors': {},
                'recommendations': []
            }
            
            # Analyze evidence
            assessment['assessment_factors'] = self._analyze_skill_evidence(skill, evidence)
            
            # Determine skill level
            assessment['skill_level'] = self._determine_skill_level(assessment['assessment_factors'])
            
            # Calculate confidence
            assessment['confidence_score'] = self._calculate_confidence_score(assessment['assessment_factors'])
            
            # Generate recommendations
            assessment['recommendations'] = self._generate_skill_recommendations(
                skill, assessment['skill_level'], assessment['assessment_factors']
            )
            
            return assessment
        except Exception as e:
            logger.error(f"Error assessing skill level: {str(e)}")
            raise
    
    def create_skill_development_plan(self, 
                                    skill_gaps: List[str], 
                                    target_career: Dict[str, Any],
                                    learning_preferences: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create comprehensive skill development plan"""
        try:
            development_plan = {
                'skill_gaps': skill_gaps,
                'target_career': target_career.get('title'),
                'learning_preferences': learning_preferences or {},
                'phases': [],
                'timeline': {},
                'resources': {},
                'milestones': [],
                'success_metrics': {}
            }
            
            # Create development phases
            development_plan['phases'] = self._create_development_phases(skill_gaps, target_career)
            
            # Estimate timeline
            development_plan['timeline'] = self._estimate_development_timeline(development_plan['phases'])
            
            # Gather resources
            development_plan['resources'] = self._gather_learning_resources(skill_gaps, learning_preferences)
            
            # Set milestones
            development_plan['milestones'] = self._set_development_milestones(development_plan['phases'])
            
            # Define success metrics
            development_plan['success_metrics'] = self._define_success_metrics(skill_gaps, target_career)
            
            return development_plan
        except Exception as e:
            logger.error(f"Error creating skill development plan: {str(e)}")
            raise
    
    def track_skill_progress(self, 
                           skill: str, 
                           progress_data: Dict[str, Any]) -> Dict[str, Any]:
        """Track progress in skill development"""
        try:
            progress_tracking = {
                'skill': skill,
                'current_level': progress_data.get('current_level', 'beginner'),
                'target_level': progress_data.get('target_level', 'intermediate'),
                'progress_percentage': 0.0,
                'milestones_completed': [],
                'next_milestones': [],
                'recommendations': []
            }
            
            # Calculate progress percentage
            progress_tracking['progress_percentage'] = self._calculate_progress_percentage(progress_data)
            
            # Track milestones
            progress_tracking['milestones_completed'] = progress_data.get('completed_milestones', [])
            progress_tracking['next_milestones'] = self._identify_next_milestones(
                skill, progress_tracking['current_level'], progress_tracking['target_level']
            )
            
            # Generate recommendations
            progress_tracking['recommendations'] = self._generate_progress_recommendations(
                skill, progress_tracking['progress_percentage'], progress_data
            )
            
            return progress_tracking
        except Exception as e:
            logger.error(f"Error tracking skill progress: {str(e)}")
            raise
    
    def _identify_skill_gaps(self, 
                           current_skills: List[str], 
                           required_skills: List[str]) -> List[str]:
        """Identify missing skills"""
        current_skills_lower = [skill.lower() for skill in current_skills]
        required_skills_lower = [skill.lower() for skill in required_skills]
        
        missing_skills = set(required_skills_lower) - set(current_skills_lower)
        return list(missing_skills)
    
    def _identify_transferable_skills(self, 
                                    current_skills: List[str], 
                                    required_skills: List[str]) -> List[str]:
        """Identify transferable skills"""
        current_skills_lower = [skill.lower() for skill in current_skills]
        required_skills_lower = [skill.lower() for skill in required_skills]
        
        transferable_skills = set(current_skills_lower) & set(required_skills_lower)
        return list(transferable_skills)
    
    def _calculate_skill_match_score(self, 
                                   current_skills: List[str], 
                                   required_skills: List[str]) -> float:
        """Calculate skill match score"""
        if not required_skills:
            return 1.0
        
        current_skills_lower = [skill.lower() for skill in current_skills]
        required_skills_lower = [skill.lower() for skill in required_skills]
        
        matching_skills = set(current_skills_lower) & set(required_skills_lower)
        return len(matching_skills) / len(required_skills_lower)
    
    def _prioritize_skill_development(self, 
                                   skill_gaps: List[str], 
                                   target_career: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Prioritize skill development"""
        priorities = []
        
        # Simple prioritization based on skill importance
        for i, skill in enumerate(skill_gaps):
            priority = {
                'skill': skill,
                'priority_level': 'high' if i < 3 else 'medium' if i < 6 else 'low',
                'importance': 'critical' if i < 2 else 'important' if i < 5 else 'nice_to_have',
                'estimated_time': self._estimate_skill_learning_time(skill),
                'difficulty': self._assess_skill_difficulty(skill)
            }
            priorities.append(priority)
        
        return priorities
    
    def _generate_learning_recommendations(self, 
                                         skill_gaps: List[str], 
                                         target_career: Dict[str, Any],
                                         student_profile: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generate learning recommendations"""
        try:
            recommendations = self.gemini_client.generate_learning_recommendations(
                [target_career.get('title', '')],
                [],  # No current skills for gap analysis
                student_profile.get('learning_style', 'visual') if student_profile else 'visual'
            )
            
            return recommendations
        except Exception as e:
            logger.error(f"Error generating learning recommendations: {str(e)}")
            return {}
    
    def _estimate_learning_timelines(self, 
                                   skill_gaps: List[str], 
                                   target_career: Dict[str, Any]) -> Dict[str, str]:
        """Estimate learning timelines for skills"""
        timelines = {}
        
        for skill in skill_gaps:
            timelines[skill] = self._estimate_skill_learning_time(skill)
        
        return timelines
    
    def _generate_skill_gap_insights(self, 
                                    current_skills: List[str], 
                                    required_skills: List[str],
                                    target_career: Dict[str, Any]) -> Dict[str, Any]:
        """Generate AI insights about skill gaps"""
        try:
            insights = self.gemini_client.analyze_skill_gaps(
                current_skills,
                target_career.get('title', ''),
                required_skills
            )
            
            return insights
        except Exception as e:
            logger.error(f"Error generating skill gap insights: {str(e)}")
            return {}
    
    def _analyze_skill_evidence(self, skill: str, evidence: List[str]) -> Dict[str, Any]:
        """Analyze evidence for skill assessment"""
        factors = {
            'experience_years': 0,
            'projects_completed': 0,
            'certifications': 0,
            'education': False,
            'work_experience': False,
            'portfolio_items': 0
        }
        
        for item in evidence:
            item_lower = item.lower()
            if 'year' in item_lower:
                factors['experience_years'] += 1
            elif 'project' in item_lower:
                factors['projects_completed'] += 1
            elif 'certification' in item_lower or 'certificate' in item_lower:
                factors['certifications'] += 1
            elif 'education' in item_lower or 'degree' in item_lower:
                factors['education'] = True
            elif 'work' in item_lower or 'job' in item_lower:
                factors['work_experience'] = True
            elif 'portfolio' in item_lower:
                factors['portfolio_items'] += 1
        
        return factors
    
    def _determine_skill_level(self, assessment_factors: Dict[str, Any]) -> str:
        """Determine skill level based on assessment factors"""
        score = 0
        
        score += assessment_factors['experience_years'] * 2
        score += assessment_factors['projects_completed'] * 1
        score += assessment_factors['certifications'] * 1
        score += 2 if assessment_factors['education'] else 0
        score += 2 if assessment_factors['work_experience'] else 0
        score += assessment_factors['portfolio_items'] * 1
        
        if score >= 8:
            return 'expert'
        elif score >= 5:
            return 'intermediate'
        elif score >= 2:
            return 'beginner'
        else:
            return 'novice'
    
    def _calculate_confidence_score(self, assessment_factors: Dict[str, Any]) -> float:
        """Calculate confidence score for assessment"""
        total_evidence = sum(assessment_factors.values())
        max_possible = 10  # Maximum possible evidence points
        
        return min(total_evidence / max_possible, 1.0)
    
    def _generate_skill_recommendations(self, 
                                     skill: str, 
                                     skill_level: str, 
                                     assessment_factors: Dict[str, Any]) -> List[str]:
        """Generate recommendations for skill development"""
        recommendations = []
        
        if skill_level == 'novice':
            recommendations.extend([
                f"Start with basic {skill} tutorials",
                f"Take an introductory {skill} course",
                f"Practice {skill} fundamentals daily"
            ])
        elif skill_level == 'beginner':
            recommendations.extend([
                f"Build {skill} projects",
                f"Join {skill} communities",
                f"Seek {skill} mentorship"
            ])
        elif skill_level == 'intermediate':
            recommendations.extend([
                f"Work on advanced {skill} projects",
                f"Teach {skill} to others",
                f"Get {skill} certification"
            ])
        else:  # expert
            recommendations.extend([
                f"Lead {skill} initiatives",
                f"Contribute to {skill} open source",
                f"Mentor others in {skill}"
            ])
        
        return recommendations
    
    def _create_development_phases(self, 
                                 skill_gaps: List[str], 
                                 target_career: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create development phases"""
        phases = []
        
        # Phase 1: Foundation skills
        foundation_skills = skill_gaps[:3] if len(skill_gaps) >= 3 else skill_gaps
        phases.append({
            'phase': 'Foundation',
            'duration': '1-3 months',
            'skills': foundation_skills,
            'focus': 'Core competencies',
            'milestones': [f"Complete {skill} basics" for skill in foundation_skills]
        })
        
        # Phase 2: Intermediate skills
        if len(skill_gaps) > 3:
            intermediate_skills = skill_gaps[3:6] if len(skill_gaps) >= 6 else skill_gaps[3:]
            phases.append({
                'phase': 'Intermediate',
                'duration': '3-6 months',
                'skills': intermediate_skills,
                'focus': 'Practical application',
                'milestones': [f"Build {skill} projects" for skill in intermediate_skills]
            })
        
        # Phase 3: Advanced skills
        if len(skill_gaps) > 6:
            advanced_skills = skill_gaps[6:]
            phases.append({
                'phase': 'Advanced',
                'duration': '6-12 months',
                'skills': advanced_skills,
                'focus': 'Expertise development',
                'milestones': [f"Master {skill}" for skill in advanced_skills]
            })
        
        return phases
    
    def _estimate_development_timeline(self, phases: List[Dict[str, Any]]) -> Dict[str, str]:
        """Estimate overall development timeline"""
        total_months = 0
        
        for phase in phases:
            duration = phase['duration']
            if '1-3' in duration:
                total_months += 2
            elif '3-6' in duration:
                total_months += 4
            elif '6-12' in duration:
                total_months += 9
        
        return {
            'total_duration': f"{total_months} months",
            'phases': len(phases),
            'estimated_completion': f"{total_months} months from start"
        }
    
    def _gather_learning_resources(self, 
                                 skill_gaps: List[str], 
                                 learning_preferences: Dict[str, Any]) -> Dict[str, List[Dict[str, str]]]:
        """Gather learning resources"""
        resources = {}
        
        for skill in skill_gaps:
            resources[skill] = [
                {
                    'type': 'Online Course',
                    'name': f'{skill} Fundamentals',
                    'url': f'https://example.com/courses/{skill.lower().replace(" ", "-")}',
                    'duration': '4-6 weeks'
                },
                {
                    'type': 'Book',
                    'name': f'Learn {skill}',
                    'url': f'https://example.com/books/{skill.lower().replace(" ", "-")}',
                    'duration': '2-4 weeks'
                },
                {
                    'type': 'Practice Project',
                    'name': f'{skill} Project',
                    'url': f'https://example.com/projects/{skill.lower().replace(" ", "-")}',
                    'duration': '1-2 weeks'
                }
            ]
        
        return resources
    
    def _set_development_milestones(self, phases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Set development milestones"""
        milestones = []
        
        for phase in phases:
            for milestone in phase['milestones']:
                milestones.append({
                    'milestone': milestone,
                    'phase': phase['phase'],
                    'estimated_completion': phase['duration'],
                    'success_criteria': f"Demonstrate {milestone.lower()}"
                })
        
        return milestones
    
    def _define_success_metrics(self, 
                               skill_gaps: List[str], 
                               target_career: Dict[str, Any]) -> Dict[str, Any]:
        """Define success metrics"""
        return {
            'skill_completion_rate': f"{len(skill_gaps)} skills to master",
            'career_readiness_score': '80%+ match with requirements',
            'project_completion': 'Complete 3+ projects per skill',
            'certification_goals': 'Obtain relevant certifications',
            'portfolio_building': 'Build comprehensive portfolio'
        }
    
    def _estimate_skill_learning_time(self, skill: str) -> str:
        """Estimate learning time for a skill"""
        # Simple heuristic based on skill complexity
        skill_lower = skill.lower()
        
        if any(tech in skill_lower for tech in ['programming', 'coding', 'software']):
            return '3-6 months'
        elif any(soft in skill_lower for soft in ['communication', 'leadership', 'teamwork']):
            return '1-3 months'
        elif any(analytical in skill_lower for analytical in ['analysis', 'data', 'research']):
            return '2-4 months'
        else:
            return '1-2 months'
    
    def _assess_skill_difficulty(self, skill: str) -> str:
        """Assess skill difficulty"""
        skill_lower = skill.lower()
        
        if any(tech in skill_lower for tech in ['programming', 'coding', 'machine learning', 'ai']):
            return 'high'
        elif any(analytical in skill_lower for analytical in ['analysis', 'data', 'research']):
            return 'medium'
        else:
            return 'low'
    
    def _calculate_progress_percentage(self, progress_data: Dict[str, Any]) -> float:
        """Calculate progress percentage"""
        completed_milestones = len(progress_data.get('completed_milestones', []))
        total_milestones = progress_data.get('total_milestones', 1)
        
        return (completed_milestones / total_milestones) * 100
    
    def _identify_next_milestones(self, 
                                skill: str, 
                                current_level: str, 
                                target_level: str) -> List[str]:
        """Identify next milestones"""
        milestones = []
        
        if current_level == 'novice' and target_level in ['beginner', 'intermediate', 'expert']:
            milestones.append(f"Complete {skill} basics")
        
        if current_level in ['novice', 'beginner'] and target_level in ['intermediate', 'expert']:
            milestones.append(f"Build {skill} project")
        
        if current_level in ['novice', 'beginner', 'intermediate'] and target_level == 'expert':
            milestones.append(f"Master {skill} advanced concepts")
        
        return milestones
    
    def _generate_progress_recommendations(self, 
                                         skill: str, 
                                         progress_percentage: float, 
                                         progress_data: Dict[str, Any]) -> List[str]:
        """Generate progress recommendations"""
        recommendations = []
        
        if progress_percentage < 25:
            recommendations.extend([
                f"Increase {skill} practice time",
                f"Find {skill} learning resources",
                f"Set {skill} learning goals"
            ])
        elif progress_percentage < 50:
            recommendations.extend([
                f"Build {skill} projects",
                f"Join {skill} communities",
                f"Seek {skill} feedback"
            ])
        elif progress_percentage < 75:
            recommendations.extend([
                f"Teach {skill} to others",
                f"Take advanced {skill} courses",
                f"Apply {skill} in real projects"
            ])
        else:
            recommendations.extend([
                f"Lead {skill} initiatives",
                f"Mentor others in {skill}",
                f"Contribute to {skill} community"
            ])
        
        return recommendations
