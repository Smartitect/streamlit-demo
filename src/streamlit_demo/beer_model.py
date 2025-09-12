import numpy as np
import polars as pl
import plotly.express as px
from typing import Tuple, Optional


class BeerWaitTimeModel:
    """
    A model that generates lognormal distributions of beer wait times
    based on the number of people attending an event and the number of bar staff.
    """
    
    @staticmethod
    def calculate_parameters(num_people: int, number_of_bar_staff: int = 1) -> Tuple[float, float]:
        """
        Calculate mu and sigma parameters for lognormal distribution
        based on number of people attending the event and bar staff.
        
        Args:
            num_people: Number of people attending the event
            number_of_bar_staff: Number of bar staff serving
        
        Returns:
            Tuple of (mu, sigma) parameters for lognormal distribution
        """
        base_mu = 1.0  # ln(mean) for ~3 minutes base wait time
        base_sigma = 0.5  # Standard deviation in log space
        crowd_factor = np.log(1 + num_people / 50)  # Logarithmic scaling
        staff_effect = np.log(1 + number_of_bar_staff)
        staff_factor = 1 / staff_effect  # More staff, smaller factor
        mu = base_mu + crowd_factor * 0.8 * staff_factor
        sigma = base_sigma + crowd_factor * 0.3 * staff_factor
        
        return mu, sigma
    
    @staticmethod
    def generate_wait_times(num_people: int, number_of_bar_staff: int = 1, random_seed: Optional[int] = None) -> pl.DataFrame:
        """
        Generate beer wait times for each person at an event.
        
        Args:
            num_people: Number of people attending the event
            number_of_bar_staff: Number of bar staff serving
            random_seed: Optional seed for reproducible results
        
        Returns:
            Array of wait times in minutes for each person
        """
        if random_seed is not None:
            np.random.seed(random_seed)
            
        mu, sigma = BeerWaitTimeModel.calculate_parameters(num_people, number_of_bar_staff)
        
        # Generate lognormal distribution
        wait_times = np.random.lognormal(mu, sigma, num_people)
        
        wait_times_df = pl.DataFrame(
            {"attendee_id": np.arange(1, num_people + 1), "wait_time_minutes": wait_times}
        )

        return wait_times_df
    
    @staticmethod
    def get_statistics(wait_times_df: pl.DataFrame) -> dict:
        """
        Get statistical summary of wait times for a given event size.
        
        Args:
            wait_times_df: DataFrame containing wait times for each attendee
        """
        return {
            'num_people': wait_times_df.shape[0],
            'mean_wait_minutes': wait_times_df['wait_time_minutes'].mean(),
            'std_wait_minutes': wait_times_df['wait_time_minutes'].std(),
            'median_wait_minutes': wait_times_df['wait_time_minutes'].median(),
            'p25_wait_minutes': wait_times_df['wait_time_minutes'].quantile(0.25),
            'p75_wait_minutes': wait_times_df['wait_time_minutes'].quantile(0.75),
            'p90_wait_minutes': wait_times_df['wait_time_minutes'].quantile(0.90),
            'max_wait_minutes': wait_times_df['wait_time_minutes'].max(),
        }
    
    @staticmethod
    def create_wait_time_histogram(wait_times_df: pl.DataFrame, num_bins: int = 30):
        """
        Create a histogram of wait times.

        Args:
            wait_times_df: DataFrame containing wait times for each attendee
            num_bins: Number of bins for the histogram

        Returns:
            A Plotly histogram figure
        """
        chart = px.histogram(
            wait_times_df,
            x='wait_time_minutes',
            title="Distribution of Beer Wait Times",
            labels={'wait_time_minutes': 'Wait Time (minutes)'},
            nbins=num_bins,
        )
        chart.update_layout(showlegend=False)
        return chart
