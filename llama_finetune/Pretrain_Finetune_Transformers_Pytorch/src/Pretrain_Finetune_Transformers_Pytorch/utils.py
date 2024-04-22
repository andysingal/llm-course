"""
Put random functions I create that need implemented and added to package.
"""

def plot_figure_image(images_details, title, save_name_path, magnify=3.5, show=True, use_dpi=None):
  """
  Plot multiple image side-by-side on a horizontal axis.
  Great to compare target-prediction.

  Args:
      images_details (list): List of dictionary that contains images details.
          Here are arguments for dictionary image details:
          'image' (numpy): image to plot.
          'title' (str): Title of the image.
      
      title (str): Title of entire figure. It can be large.

      save_name_path (str): Path where to save figure + name of figure.

      magnify (float): Multiply weights and height by magnify value. 
          Helps zoom in or out figure.

      show (bool): To show the plot or not. If use in headless server no need to show plot.

      use_dpi (int): The dpi of the figure plot. The larger the higher the quality.
  """
  import matplotlib.pyplot as plt
  # Get figure and axes array.
  figure, axarr = plt.subplots(1,len(images_details), )
  # For each ax array add sybplot.
  for index, image_details in enumerate(images_details):
    # Add subplot image.
    axarr[index].imshow(image_details['image'])
    # Add title to subplot.
    axarr[index].set_title(image_details['title'], fontsize=16)
  # Add figure title.
  figure.suptitle(title, fontsize=16, horizontalalignment='left', y=0.75)
  # figure.subplots_adjust(top=1.0)
  figure.tight_layout()
  # Get size of figure.
  figsize = figure.get_size_inches()
  # Change size depending on magnify.
  figsize = [figsize[0] * magnify, figsize[1] * magnify]
  figure.set_size_inches(figsize)
  # Set the new figure size.
  figure.savefig(save_name_path, bbox_inches='tight', pad_inches=0.1, dpi=use_dpi)
  # Show plot.
  plt.show() if show else None #print("Not showing figure. It is saved in '{}'.")
  # Close figure.
  plt.close(figure)


def evaluate_classification(target, prediction):
  """
  Compute metrics for classificaiton evlauation.

  Great source: https://datascience.stackexchange.com/a/26855
  """

  # Make sure confusion matrix is imported.
  from sklearn.metrics import confusion_matrix
  # Run confusion matrix over target and prediction
  tn, fp, fn, tp = confusion_matrix(y_true=target, y_pred=prediction).ravel()
  
  # Compute various metrics
  # Precision: (or Positive predictive value)
  # proportion of predicted positives which are actual positive
  ppv = tp/(tp+fp) if (tp+fp) != 0 else 0
  # Sensitivity, hit rate, recall, or true positive rate
  # proportion of actual positives which are predicted positive
  tpr = tp/(tp+fn) if (tp+fn) != 0 else 0
  # Specificity or true negative rate
  # proportion of actual negative which are predicted negative
  tnr = tn/(tn+fp) if (tn+fp) != 0 else 0
  # Negative predictive value
  npv = tn/(tn+fn) if (tn+fn) != 0 else 0
  # Fall out or false positive rate
  fpr = fp/(fp+tn) if (fp+tn) != 0 else 0
  # False negative rate
  fnr = fn/(tp+fn) if (tp+fn) != 0 else 0
  # False discovery rate
  fdr = fp/(tp+fp) if (tp+fp) != 0 else 0
  # F1 score
  f1 = (2*tp)/(2*tp+fp+fn) if (2*tp+fp+fn) != 0 else 0
  # Overall accuracy
  acc = (tp+tn)/(tp+fp+fn+tn) if (tp+fp+fn+tn) != 0 else 0
  # BCR: Balanced Classification Rate: 0.5*(tp/(tp+fn)+tn/(tn+fp))
  bcr = 0.5*(tpr+tnr)
  # Balanced Error Rate, or HTER: 1 - 0.5 * (tp/(tp+fn)+tn/(tn+fp))
  ber = 1-0.5*(tpr+tnr)

  # Return metrics as a dictionary.
  return {
          "accuracy": acc,
          "precision": ppv,
          "recall": tpr,
          "f1": f1,
          "specificity": tnr,
          'ber': ber,
          }
