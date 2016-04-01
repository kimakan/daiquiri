from django.test import TestCase
from django.core.urlresolvers import reverse

import iso8601
from lxml import objectify

from daiquiri_jobs.models import Job


class UWSTestCase(TestCase):
    fixtures = ['auth/testing.json', 'jobs/testing.json']
    uws_ns = '{http://www.ivoa.net/xml/UWS/v1.0}'

    def setUp(self):
        self.pending_job = Job.objects.filter(phase=Job.PHASE_PENDING).first()
        self.error_job = Job.objects.filter(phase=Job.PHASE_ERROR).first()

    def test_get_job_list_xml(self):
        '''
        GET /{jobs} returns the job list as <uws:jobs> xml element.
        '''
        url = reverse('uws:job-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        root = objectify.fromstring(response.content)
        self.assertEqual(root.tag, self.uws_ns + 'jobs')
        self.assertEqual(root.jobref.tag, self.uws_ns + 'jobref')

    def test_get_job_list_xml_phase(self):
        '''
        GET /{jobs}?PHASE=<phase> returns the filtered joblist as <jobs>
        element.
        '''
        url = reverse('uws:job-list') + '?PHASE=PENDING&PHASE=ARCHIVED'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        root = objectify.fromstring(response.content)
        self.assertEqual(len(root.jobref), 2)

    def test_get_job_list_xml_after(self):
        '''
        GET /{jobs}?AFTER=2014-09-10T10:01:02.000 returns jobs with startTimes
        after the given [std:iso8601] time in UTC.
        '''
        url = reverse('uws:job-list') + '?AFTER=2015-01-01T00:00:00'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        root = objectify.fromstring(response.content)
        self.assertEqual(len(root.jobref), 6)

    def test_get_job_list_xml_last(self):
        '''
        GET /{jobs}?LAST=100 returns the given number of most recent jobs
        ordered by ascending startTimes.
        '''
        url = reverse('uws:job-list') + '?LAST=3'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        root = objectify.fromstring(response.content)
        self.assertEqual(len(root.jobref), 3)

        # '''
        # POST /{jobs} with an application/x-www-form-urlencoded set of
        # KEY=VALUE and additionally PHASE=RUN to an non-existing {job-id} creates
        # a job with these parameters and runs it.
        # '''

        # '''
        # POST /{jobs} with an application/x-www-form-urlencoded set of
        # KEY=VALUE to an existing {job-id} updates the parameters.
        # '''

    def test_get_job_detail(self):
        '''
        GET /{jobs}/{job-id} returns a job as <uws:job> xml element.
        '''
        url = reverse('uws:job-detail', args=[self.pending_job.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        root = objectify.fromstring(response.content)
        self.assertEqual(root.tag, self.uws_ns + 'job')

    def test_get_job_results(self):
        '''
        GET /{jobs}/{job-id}/results returns any results of the job {job-id} as
        <uws:results> xml element.
        '''
        url = reverse('uws:job-results', args=[self.pending_job.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        root = objectify.fromstring(response.content)
        self.assertEqual(root.tag, self.uws_ns + 'results')
        self.assertEqual(root.result.tag, self.uws_ns + 'result')

    def test_get_job_parameters(self):
        '''
        GET /{jobs}/{job-id}/parameters returns any parameters for the job
        {job-id} as <uws:parameters> xml element.
        '''
        url = reverse('uws:job-parameters', args=[self.pending_job.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        root = objectify.fromstring(response.content)
        self.assertEqual(root.tag, self.uws_ns + 'parameters')
        self.assertEqual(root.parameter.tag, self.uws_ns + 'parameter')

        # '''
        # POST /{jobs}/{job-id}/parameters with application/x-www-form-urlencoded
        # set of KEY=VALUE updates the parameters.
        # '''

    def test_get_job_error(self):
        '''
        GET /{jobs}/{job-id}/error returns any error message associated with
        {job-id} as text.
        '''
        url = reverse('uws:job-error', args=[self.error_job.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_get_job_delete(self):
        '''
        DELETE /{jobs}/{job-id} sets the job phase to ARCHIVED and deletes the
        results and redirects to /{jobs}/{job-id} as 303.
        '''
        url = reverse('uws:job-detail', args=[self.error_job.pk])
        response = self.client.delete(url)
        self.assertRedirects(response, url, status_code=303)
        self.assertEqual(self.error_job.phase, Job.PHASE_ERROR)

        # '''
        # POST /{jobs}/{job-id} with ACTION=DELETE sets the job phase to ARCHIVED
        # and deletes the results and redirects to /{jobs}/{job-id} as 303.
        # '''

    def test_get_job_destruction(self):
        '''
        GET /{jobs}/{job-id}/destruction returns the destruction instant for
        {job-id} as [std:iso8601].
        '''
        url = reverse('uws:job-destruction', args=[self.error_job.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '')

    def test_post_job_destruction(self):
        '''
        POST /{jobs}/{job-id}/destruction with DESTRUCTION={std:iso8601}
        (application/x-www-form-urlencoded) sets the destruction instant for
        {job-id} and redirects to /{jobs}/{job-id} as 303.
        '''
        destruction_time = '2016-01-01T00:00:00'

        url = reverse('uws:job-destruction', args=[self.pending_job.pk])
        response = self.client.post(url, 'DESTRUCTION=%s' % destruction_time, content_type='application/x-www-form-urlencoded')
        self.assertRedirects(response, reverse('uws:job-detail', args=[self.pending_job.pk]), status_code=303)
        self.assertEqual(
            Job.objects.get(pk=self.pending_job.pk).destruction_time,
            iso8601.parse_date('2016-01-01T00:00:00')
        )

    def test_get_job_executionduration(self):
        '''
        GET /{jobs}/{job-id}/executionduration returns the maximum execution
        duration of {job-id} as integer.
        '''
        url = reverse('uws:job-executionduration', args=[self.pending_job.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '30')

    def test_post_job_executionduration(self):
        '''
        POST /{jobs}/{job-id}/executionduration with EXECUTIONDURATION={int}
        sets the maximum execution duration of {job-id} and redirects as to
        /{jobs}/{job-id} 303.
        '''
        execution_duration = 60

        url = reverse('uws:job-executionduration', args=[self.pending_job.pk])
        response = self.client.post(url, 'EXECUTIONDURATION=%i' % execution_duration, content_type='application/x-www-form-urlencoded')
        self.assertRedirects(response, reverse('uws:job-detail', args=[self.pending_job.pk]), status_code=303)
        self.assertEqual(
            Job.objects.get(pk=self.pending_job.pk).execution_duration,
            execution_duration
        )

    def test_get_job_phase(self):
        '''
        GET /{jobs}/{job-id}/phase returns the phase of job {job-id} as one of
        the fixed strings.
        '''
        url = reverse('uws:job-phase', args=[self.pending_job.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'PENDING')

    def test_post_job_phase_run(self):
        '''
        POST /{jobs}/{job-id}/phase with PHASE=RUN runs the job {job-id} and
        redirects as to /{jobs}/{job-id} 303.
        '''
        url = reverse('uws:job-phase', args=[self.pending_job.pk])
        response = self.client.post(url, 'PHASE=RUN', content_type='application/x-www-form-urlencoded')
        self.assertRedirects(response, reverse('uws:job-detail', args=[self.pending_job.pk]), status_code=303)
        self.assertEqual(Job.objects.get(pk=self.pending_job.pk).phase, Job.PHASE_QUEUED)

    def test_post_job_phase_abort(self):
        '''
        POST /{jobs}/{job-id}/phase with PHASE=ABORT aborts the job {job-id} and
        redirects as to /{jobs}/{job-id} 303.
        '''
        url = reverse('uws:job-phase', args=[self.pending_job.pk])
        response = self.client.post(url, 'PHASE=ABORT', content_type='application/x-www-form-urlencoded')
        self.assertRedirects(response, reverse('uws:job-detail', args=[self.pending_job.pk]), status_code=303)
        self.assertEqual(Job.objects.get(pk=self.pending_job.pk).phase, Job.PHASE_ABORTED)

    def test_get_job_quote(self):
        '''
        GET /{jobs}/{job-id}/quote returns the quote for {job-id} as [std:iso8601].
        '''
        url = reverse('uws:job-quote', args=[self.pending_job.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '')

    def test_get_job_owner(self):
        '''
        GET /{jobs}/{job-id}/owner returns the owner of the job {job-id} as an
        appropriate identifier.
        '''
        url = reverse('uws:job-owner', args=[self.pending_job.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'admin')
